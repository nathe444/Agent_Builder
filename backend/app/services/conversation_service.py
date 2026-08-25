from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.conversation import Conversation
from app.models.chatbot import Chatbot
from app.models.user import User


class ConversationService:

    @staticmethod
    def create_conversation(
        chatbot_id: int,
        current_user: User,
        db: Session,
        title: str | None = None
    ):

        chatbot = (
            db.query(Chatbot)
            .filter(
                Chatbot.id == chatbot_id,
                Chatbot.user_id == current_user.id
            )
            .first()
        )

        if not chatbot:
            raise HTTPException(
                status_code=404,
                detail="Chatbot not found"
            )

        conversation = Conversation(
            chatbot_id=chatbot.id,
            user_id=current_user.id,
            title=title
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_conversation(
        conversation_id: int,
        current_user: User,
        db: Session
    ):

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
            .first()
        )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        return conversation

    @staticmethod
    def get_conversations(
        chatbot_id: int,
        current_user: User,
        db: Session
    ):

        return (
            db.query(Conversation)
            .filter(
                Conversation.chatbot_id == chatbot_id,
                Conversation.user_id == current_user.id
            )
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete_conversation(
        conversation_id: int,
        current_user: User,
        db: Session
    ):

        conversation = ConversationService.get_conversation(
            conversation_id,
            current_user,
            db
        )

        db.delete(conversation)

        db.commit()

        return {
            "message": "Conversation deleted successfully"
        }


conversation_service = ConversationService()