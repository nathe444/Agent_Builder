import json

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

from fastapi.responses import StreamingResponse

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


@router.post(
    "/conversations/{conversation_id}/messages/stream"
)
def chat_stream(
    conversation_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    def event_generator():
        for token in chat_service.chat_stream(
            conversation_id=conversation_id,
            question=request.question,
            current_user=current_user,
            db=db,
        ):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )