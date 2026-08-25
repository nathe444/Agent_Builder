from app.dependencies.auth import get_current_user
from app.database import db
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.database.db import get_db
from app.models.user import User
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest


class AuthService:

    @staticmethod
    def register(
        user: UserCreate,
        db: Session
    ):

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
        )

        new_user = User(
            name=user.name,
            email=user.email,
            password_hash=hash_password(
                user.password
            )
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return new_user


    @staticmethod
    def login(
        credentials: LoginRequest,
        db: Session
    ):
        user = db.query(User).filter(
            User.email == credentials.email
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(
            credentials.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token({
            "sub": str(user.id)
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    @staticmethod
    def get_me(
        current_user: User
    ):
        return current_user

auth_service = AuthService()