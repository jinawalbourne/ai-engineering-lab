import re

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import check_database_connection
from app.database import engine
from app.models import User


app = FastAPI(title="AI Engineering Lab")


class RegistrationRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("invalid email address")
        return value


class UserResponse(BaseModel):
    id: int
    email: str


@app.get("/health", response_model=None)
def health_check():
    if check_database_connection():
        return {"status": "healthy"}

    return JSONResponse(
        status_code=503,
        content={"status": "unhealthy"},
    )


@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register_user(request: RegistrationRequest) -> UserResponse:
    with Session(engine) as session:
        existing_user = session.scalar(
            select(User).where(User.email == request.email)
        )
        if existing_user is not None:
            return JSONResponse(
                status_code=409,
                content={"detail": "email already registered"},
            )

        user = User(
            email=request.email,
            password_hash=hash_password(request.password),
        )
        session.add(user)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return JSONResponse(
                status_code=409,
                content={"detail": "email already registered"},
            )

        session.refresh(user)
        return UserResponse(id=user.id, email=user.email)
