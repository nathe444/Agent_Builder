from app.models import document_chunk
from app.models import document_chunk
from app.ingestion.ingestion_service import ingestion_service
from app import database
from app.schemas.document import DocumentResponse
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.chatbot import Chatbot
from app.models.document import Document
import os
from app.schemas.document import UrlDocumentCreate
from app.storage.supabase_storage import supabase_storage
from app.tasks.document_tasks import process_document

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
    ".md",
    ".json",
    ".doc"
}


class DocumentService:

    @staticmethod
    async def upload_document(
    chatbot_id: int,
    file: UploadFile,
    db: Session,
    current_user: User 
    ):
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.user_id == current_user.id
        ).first()

        if not chatbot:
            raise HTTPException(
                status_code=404,
                detail="Chatbot not found"
            )
            
        if file.filename == "":
            raise HTTPException(
                status_code=400,
                detail="No file uploaded"
            )

        _, file_extension = os.path.splitext(
            file.filename
        )

        if file_extension.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        file_path, file_name = await supabase_storage.upload(
            file=file,
            user_id=current_user.id,
            chatbot_id=chatbot.id
        )
        
        document = Document(
            chatbot_id=chatbot.id,
            file_name=file_name,
            file_path=file_path,
            source_type=file_extension.lower().replace(".", ""),
            status="queued"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        print("=== Starting ingestion ===")
        print(document.id)

        process_document.delay(document.id)

        db.refresh(document)
        
        return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "file_name": document.file_name,
        "source_type": document.source_type,
        "status": document.status
    }

    @staticmethod
    def add_url_document(
    payload: UrlDocumentCreate,
    db: Session ,
    current_user: User 
    ):
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == payload.chatbot_id,
            Chatbot.user_id == current_user.id
        ).first()

        if not chatbot:
            raise HTTPException(
                status_code=404,
                detail="Chatbot not found"
            )

        document = Document(
            chatbot_id=chatbot.id,
            source_type="url",
            source_value=str(payload.url),
            status="uploaded"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        ingestion_service.process_document(
            document=document,
            db=db
        )

        db.refresh(document)

        return {
            "message": "URL added successfully",
            "document_id": document.id,
            "status": document.status
        }


    @staticmethod
    def get_documents(
    chatbot_id: int,
    db: Session ,
    current_user: User 
    ):
        chatbot = db.query(Chatbot).filter(
            Chatbot.id == chatbot_id,
            Chatbot.user_id == current_user.id
        ).first()

        if not chatbot:
            raise HTTPException(
                status_code=404,
                detail="Chatbot not found"
            )
        
        return db.query(Document).filter(
            Document.chatbot_id == chatbot_id
        ).all()


    @staticmethod
    def get_document(
    document_id: int,
    db: Session,
    current_user: User 
    ):
        document = (
        db.query(Document)
        .join(Chatbot)
        .filter(
            Document.id == document_id,
            Chatbot.user_id == current_user.id
        )
        .first()
    )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        return document
        

    @staticmethod
    def delete_document(
    document_id: int,
    db: Session,
    current_user: User 
    ):
        print(f"ENTERED delete_document with id={document_id}")

        document = (
            db.query(Document)
            .join(Chatbot)
            .filter(
                Document.id == document_id,
                Chatbot.user_id == current_user.id
            )
            .first()
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        print(f"CHECK: source_type={document.source_type!r}, file_path={document.file_path!r}")
        
        if document.source_type != "url" and document.file_path:
            try:

                result = supabase_storage.delete(document.file_path)

            except Exception:
                import traceback
                traceback.print_exc()
                raise
            
        db.delete(document)
        db.commit()
        return {
            "message": "Document deleted successfully"
        }

document_service = DocumentService()