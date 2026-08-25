from pydantic import BaseModel


class ChatRequest(BaseModel):
    
    question: str

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.models.user import User

from app.dependencies.auth import (
    get_current_user
)

from app.schemas.chat import (
    ChatRequest
)

from app.services.chat_service import (
    chat_service
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/conversations/{conversation_id}/messages"
)
def chat(
    conversation_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return chat_service.chat(
        conversation_id=conversation_id,
        question=request.question,
        current_user=current_user,
        db=db,
    )