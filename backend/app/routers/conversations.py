from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.db import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.services.conversation_service import conversation_service
from app.services.message_service import message_service


router = APIRouter(tags=["Conversations"])


# ── Schemas ─────────────────────────────────────────────

class CreateConversationRequest(BaseModel):
    title: str | None = None


class ConversationResponse(BaseModel):
    id: int
    chatbot_id: int
    user_id: int
    title: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    citations: Optional[list] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Routes ──────────────────────────────────────────────

@router.post(
    "/chatbots/{chatbot_id}/conversations",
    response_model=ConversationResponse,
)
def create_conversation(
    chatbot_id: int,
    request: CreateConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return conversation_service.create_conversation(
        chatbot_id=chatbot_id,
        current_user=current_user,
        db=db,
        title=request.title,
    )


@router.get(
    "/chatbots/{chatbot_id}/conversations",
    response_model=list[ConversationResponse],
)
def get_conversations(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return conversation_service.get_conversations(
        chatbot_id=chatbot_id,
        current_user=current_user,
        db=db,
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = conversation_service.get_conversation(
        conversation_id=conversation_id,
        current_user=current_user,
        db=db,
    )
    return message_service.get_messages(
        conversation=conversation,
        db=db,
    )


@router.delete(
    "/conversations/{conversation_id}",
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return conversation_service.delete_conversation(
        conversation_id=conversation_id,
        current_user=current_user,
        db=db,
    )
