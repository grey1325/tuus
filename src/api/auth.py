import os
from fastapi import APIRouter, HTTPException, Request
from passlib.context import CryptContext
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)
users_db = {}


class UserResponse(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(char.isalpha() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну букву")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return value


@router.post("/register", response_model=UserResponse)
@limiter.limit("3/minute")
def register(request: Request, user: UserCreate):
    if user.username in users_db:
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже существует",
        )
    user_id = len(users_db) + 1
    users_db[user.username] = {
        "id": user_id,
        "username": user.username,
        "hashed_password": pwd_context.hash(user.password),
    }
    return {"id": user_id, "username": user.username}


@router.post("/login")
@limiter.limit(os.getenv("RATE_LIMIT_LOGIN", "5/minute"))
def login_user(request: Request, data: LoginRequest):
    user = users_db.get(data.username)
    if not user or not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Неверные учетные данные",
        )
    return {
        "message": "Авторизация успешна",
        "user_id": user["id"],
    }
