from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse
from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

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


@router.post("/upload/{chatbot_id}")
async def upload_document(
    chatbot_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await DocumentService.upload_document(chatbot_id , file , db , current_user)


@router.post("/url")
def add_url_document(
    payload: UrlDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.add_url_document(payload , db , current_user)
        

@router.get(
    "/chatbot/{chatbot_id}",
    response_model=list[DocumentResponse]
)
def get_documents(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.get_documents(chatbot_id , db , current_user)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.get_document(document_id,db,current_user)

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.delete_document(document_id, db, current_user)