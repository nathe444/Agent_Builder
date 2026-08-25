from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import Text

from app.database.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    chatbot_id = Column(
        Integer,
        ForeignKey("chatbots.id")
    )

    file_name = Column(String)

    file_path = Column(String)

    source_type = Column(String)

    source_value = Column(String)

    status = Column(String)

    chunks_count = Column(Integer)

    embedding_status = Column(
        String,
        default="pending"
    )

    processed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    processing_error = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chatbot = relationship(
        "Chatbot",
        back_populates="documents"
    )

    chunks = relationship(
    "DocumentChunk",
    back_populates="document",
    cascade="all, delete-orphan"
    )
