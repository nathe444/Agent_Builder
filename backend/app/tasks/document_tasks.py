from app.core.celery import celery_app
import app.models
from app.database.db import SessionLocal
from app.models.document import Document
from app.ingestion.ingestion_service import ingestion_service
from app.services.document_embedding_service import document_embedding_service


@celery_app.task(name="app.tasks.document_tasks.process_document")
def process_document(document_id: int):

    db = SessionLocal()

    try:

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        if not document:
            print(f"Document {document_id} not found.")
            return

        ingestion_service.process_document(
            document=document,
            db=db
        )

        document_embedding_service.embed_document(
            document_id=document.id,
            db=db
        )

    finally:
        db.close()