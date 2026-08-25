from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.chatbot import ChatbotUpdate
from app.database.db import get_db
from fastapi import HTTPException
from app.models.chatbot import Chatbot
from app.schemas.chatbot import (
    ChatbotCreate,
    ChatbotResponse
)
from app.dependencies.auth import (
    get_current_user
)
from app.models.user import User
from app.services.chatbot_service import ChatbotService


router = APIRouter(
    prefix="/chatbots",
    tags=["Chatbots"]
)

@router.post(
    "/",
    response_model=ChatbotResponse
)
def create_chatbot(
    chatbot: ChatbotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatbotService.create_chatbot(chatbot, db, current_user)

    

@router.get(
    "/",
    response_model=list[ChatbotResponse]
)
def get_chatbots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatbotService.get_chatbots(db, current_user)
    
    
@router.get(
    "/{chatbot_id}",
    response_model=ChatbotResponse
)
def get_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatbotService.get_chatbot(chatbot_id, db, current_user)


@router.put(
    "/{chatbot_id}",
    response_model=ChatbotResponse
)
def update_chatbot(
    chatbot_id: int,
    chatbot_data: ChatbotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatbotService.update_chatbot(chatbot_id,chatbot_data,db,current_user)


@router.delete("/{chatbot_id}")
def delete_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChatbotService.delete_chatbot(chatbot_id,db,current_user)