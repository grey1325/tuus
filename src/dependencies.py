from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.order_service import OrderService
from src.database.repositories.order_repository import OrderRepository
from src.services.user_service import UserService
from src.database.repositories.user_repository import UserRepository
from src.database.connection import get_async_db
from src.services.product_service import ProductService
from src.database.repositories.product_repository import ProductRepository


async def get_product_repository(
    session: AsyncSession = Depends(get_async_db),
) -> ProductRepository:
    return ProductRepository(session)


async def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    return ProductService(product_repo)


async def get_user_repository(
    session: AsyncSession = Depends(get_async_db),
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


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
