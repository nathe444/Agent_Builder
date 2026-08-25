from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.embeddings.embedding_service import (
    embedding_service
)


class DocumentEmbeddingService:

    BATCH_SIZE = 96

    @staticmethod
    def embed_document(
        document_id: int,
        db: Session
    ):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise Exception("Document not found.")

        try:

            document.embedding_status = "processing"
            document.embedding_error = None

            db.commit()

            chunks = (
                db.query(DocumentChunk)
                .filter(
                    DocumentChunk.document_id == document.id
                )
                .order_by(
                    DocumentChunk.chunk_index
                )
                .all()
            )

            if not chunks:

                document.embedding_status = "failed"
                document.embedding_error = (
                    "No chunks found."
                )

                db.commit()

                return

            for start in range(
                0,
                len(chunks),
                DocumentEmbeddingService.BATCH_SIZE
            ):

                batch = chunks[
                    start:
                    start + DocumentEmbeddingService.BATCH_SIZE
                ]

                texts = [
                    chunk.content
                    for chunk in batch
                ]

                embeddings = (
                    embedding_service
                    .embed_texts(texts)
                )

                for chunk, embedding in zip(
                    batch,
                    embeddings
                ):

                    chunk.embedding = embedding

                db.commit()

            document.embedding_status = "completed"
            document.embedding_error = None

            db.commit()

            print(
                f"Embedded {len(chunks)} chunks."
            )

        except Exception as e:

            db.rollback()

            document.embedding_status = "failed"
            document.embedding_error = str(e)

            db.commit()

            raise


document_embedding_service = (
    DocumentEmbeddingService()
)