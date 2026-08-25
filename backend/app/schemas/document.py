from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional


class DocumentResponse(BaseModel):
    id: int
    file_name: Optional[str] = None
    source_type: str
    status: str
    created_at: datetime
    source_value: Optional[str] = None

    class Config:
        from_attributes = True

class UrlDocumentCreate(BaseModel):
    chatbot_id: int
    url: HttpUrl