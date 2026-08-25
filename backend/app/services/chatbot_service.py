from app import database
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.chatbot import Chatbot
from app.schemas.chatbot import ChatbotCreate
from fastapi import HTTPException
from app.schemas.chatbot import ChatbotUpdate


class ChatbotService:
    @staticmethod
    def create_chatbot(
        chatbot: ChatbotCreate,
        db: Session,
        current_user: User
    ):

        new_chatbot = Chatbot(
            **chatbot.model_dump(),
            user_id=current_user.id
        )

        db.add(new_chatbot)

        db.commit()

        db.refresh(new_chatbot)

        return new_chatbot

    @staticmethod
    def get_chatbots(
        db: Session ,
        current_user: User
    ):
        return db.query(Chatbot).filter(
            Chatbot.user_id == current_user.id
        ).all()


    @staticmethod
    def get_chatbot(
        chatbot_id: int,
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

        return chatbot


    @staticmethod
    def update_chatbot(
    chatbot_id: int,
    chatbot_data: ChatbotUpdate,
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

        update_data = chatbot_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(chatbot, key, value)

        db.commit()
        db.refresh(chatbot)

        return chatbot
    
    @staticmethod
    def delete_chatbot(
        chatbot_id: int,
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

        db.delete(chatbot)
        db.commit()

        return {
            "message": "Chatbot deleted successfully"
        }


chatbot_service = ChatbotService()