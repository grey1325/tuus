from src.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from src.services.user_service import UserService
from src.database.models import User
from src.api.schemas import TokenResponse, UserCreate, UserLogin
from src.services.jwt_service import JwtService
from src.services.password_service import PasswordService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        jwt_service: JwtService,
        password_service: PasswordService,
    ) -> None:
        self.user_service = user_service
        self.jwt_service = jwt_service
        self.password_service = password_service

    async def register_user(self, user: UserCreate) -> User:
        user_by_email = await self.user_service.get_user_by_email(user.email)
        if user_by_email:
            raise UserAlreadyExistsError("User with this email already exists")
        password_hash = self.password_service.hash_password(user.password)
        return await self.user_service.create_user(
            name=user.name, email=user.email, password_hash=password_hash
        )

    async def authenticate_user(self, user_login: UserLogin) -> TokenResponse:
        user = await self.user_service.get_user_by_email(user_login.email)
        if user is None:
            raise InvalidCredentialsError("Invalid credentials")
        if not self.password_service.verify_password(
            user_login.password, user.password_hash
        ):
            raise InvalidCredentialsError("Invalid credentials")
        access_token = self.jwt_service.create_access_token(str(user.id))
        refresh_token = self.jwt_service.create_refresh_token(str(user.id))
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        payload = self.jwt_service.decode_token(refresh_token, "refresh")
        user = await self.user_service.get_user(int(payload["sub"]))
        access_token = self.jwt_service.create_access_token(str(user.id))
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
