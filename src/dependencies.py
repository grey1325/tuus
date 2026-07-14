from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from src.services.auth_service import AuthService
from src.services.jwt_service import JwtService
from src.services.password_service import PasswordService
from src.services.order_service import OrderService
from src.database.repositories.order_repository import OrderRepository
from src.services.user_service import UserService
from src.database.repositories.user_repository import UserRepository
from src.database.connection import get_async_db
from src.services.product_service import ProductService
from src.database.repositories.product_repository import ProductRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Product
async def get_product_repository(
    session: AsyncSession = Depends(get_async_db),
) -> ProductRepository:
    return ProductRepository(session)


async def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    return ProductService(product_repo)


# User
async def get_user_repository(
    session: AsyncSession = Depends(get_async_db),
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


# Order
async def get_order_repository(
    session: AsyncSession = Depends(get_async_db),
) -> OrderRepository:
    return OrderRepository(session)


async def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
) -> OrderService:
    return OrderService(
        order_repo=order_repo, user_repo=user_repo, product_repo=product_repo
    )


# Auth
async def get_password_service():
    return PasswordService()


async def get_jwt_service():
    return JwtService()


async def get_auth_service(
    user_service: UserService = Depends(get_user_service),
    jwt_service: JwtService = Depends(get_jwt_service),
    password_service: PasswordService = Depends(get_password_service),
) -> AuthService:
    return AuthService(
        user_service=user_service,
        jwt_service=jwt_service,
        password_service=password_service,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JwtService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
) -> User:

    payload = jwt_service.decode_token(token, "access")
    user = await user_service.get_user(int(payload["sub"]))
    return user
