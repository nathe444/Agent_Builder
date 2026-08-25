from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.conversation import Conversation
from app.models.message import MessageRole


class MessageService:

    @staticmethod
    def create_message(
        conversation: Conversation,
        role: MessageRole,
        content: str,
        db: Session,
        citations=None
    ):

        message = Message(
            conversation_id=conversation.id,
            role=role,
            content=content,
            citations=citations
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def get_messages(
        conversation: Conversation,
        db: Session
    ):

        return (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation.id
            )
            .order_by(
                Message.created_at.asc()
            )
            .all()
        )

    @staticmethod
    def delete_messages(
        conversation: Conversation,
        db: Session
    ):

        (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation.id
            )
            .delete()
        )

        db.commit()


message_service = MessageService()