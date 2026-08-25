from app.services.auth_service import AuthService
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.core.security import hash_password
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest



from app.core.security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register(user, db)



@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(credentials, db)



@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return AuthService.get_me(current_user)