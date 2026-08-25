from pydantic import BaseModel


class ChatbotCreate(BaseModel):
    name: str
    description: str
    system_prompt: str
    model_name: str

class ChatbotUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    system_prompt: str | None = None
    model_name: str | None = None

class ChatbotResponse(BaseModel):
    id: int
    name: str
    description: str
    system_prompt: str
    model_name: str

    class Config:
        from_attributes = True