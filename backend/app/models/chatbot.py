from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database.db import Base


class Chatbot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    description = Column(String)

    system_prompt = Column(String)

    model_name = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="chatbots"
    )

    documents = relationship(
    "Document",
    back_populates="chatbot",
    cascade="all, delete-orphan"
   )

    conversations = relationship(
        "Conversation",
        back_populates="chatbot",
        cascade="all, delete-orphan",
    )
