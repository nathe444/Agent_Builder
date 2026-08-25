import os
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.ingestion.loader_factory import LoaderFactory
from app.ingestion.splitter import TextSplitter

from app.storage.supabase_storage import supabase_storage


class IngestionService:

    @staticmethod
    def process_document(
        document: Document,
        db: Session
    ):

        local_path = None

        try:

            # Mark document as processing
            document.status = "processing"
            db.commit()

            print("===== STARTING INGESTION =====")

            # Download only if the source is a file
            if document.source_type != "url":

                local_path = supabase_storage.download(
                    document.file_path
                )

                loader = LoaderFactory.get_loader(
                    source_type=document.source_type,
                    file_path=local_path
                )

            else:

                loader = LoaderFactory.get_loader(
                    source_type="url",
                    source_value=document.source_value
                )

            # Load into LangChain Documents
            documents = loader.load()

            print(f"Loaded {len(documents)} documents")

            for i, doc in enumerate(documents):
                print(
                    f"Document {i}: {len(doc.page_content)} characters"
                )

            # Split into chunks
            splitter = TextSplitter()

            chunks = splitter.split(documents)

            print(f"Generated {len(chunks)} chunks")

            # Remove old chunks
            db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document.id
            ).delete()

            # Save chunks
            for index, chunk in enumerate(chunks):

                db_chunk = DocumentChunk(
                    document_id=document.id,
                    chatbot_id=document.chatbot_id,
                    chunk_index=index,
                    content=chunk.page_content,
                    chunk_metadata=chunk.metadata
                )

                db.add(db_chunk)

            # Update document
            document.chunks_count = len(chunks)
            document.status = "processed"
            document.processing_error = None
            document.processed_at = datetime.now(timezone.utc)

            db.commit()

            print(
                f"Successfully processed {len(chunks)} chunks."
            )

            return chunks

        except Exception as e:

            db.rollback()

            document.status = "failed"
            document.processing_error = str(e)

            db.commit()

            raise e

        finally:

            # Remove temporary downloaded file
            if (
                local_path
                and os.path.exists(local_path)
            ):
                os.remove(local_path)


ingestion_service = IngestionService()