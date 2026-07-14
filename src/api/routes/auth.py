from fastapi import APIRouter, Depends, status

from src.dependencies import get_auth_service
from src.services.auth_service import AuthService
from src.api.schemas import (
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_create: UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register_user(user_create)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    user_login: UserLogin, auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.authenticate_user(user_login)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(
    refresh_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh_access_token(refresh_request.refresh_token)
