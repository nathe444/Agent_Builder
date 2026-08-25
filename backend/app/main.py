from app.dependencies.auth import get_current_user
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.database.db import engine
from app.database.base import Base
from app.routers import chat
from app.routers import chatbots
from app.routers import documents
from app.routers import conversations

app = FastAPI(
    title="Chatbot Builder API",
    description="API for building chatbots",
    version="1.0.0",
    # dependencies=[Depends(get_current_user)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:50251",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:50251",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(chatbots.router)

app.include_router(
    documents.router
)

app.include_router(chat.router)
app.include_router(conversations.router)

@app.get("/")
def root():
    return {
        "message": "Chatbot Platform API"
    }