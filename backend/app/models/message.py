from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    JSON,
)

from sqlalchemy import Enum
import enum
from sqlalchemy.orm import relationship

from app.database.db import Base

class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role = Column(
        Enum(MessageRole),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    citations = Column(
        JSON,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )