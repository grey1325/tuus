from unittest.mock import AsyncMock
import pytest
from src.services.jwt_service import JwtService
from src.services.password_service import PasswordService
from src.services.product_service import ProductService
from src.services.order_service import OrderService
from src.services.user_service import UserService


@pytest.fixture
def order_service_mock():
    order_repo = AsyncMock()
    user_repo = AsyncMock()
    product_repo = AsyncMock()
    service = OrderService(order_repo, user_repo, product_repo)
    return service, order_repo, user_repo, product_repo


@pytest.fixture
def product_service_mock():
    product_repo = AsyncMock()
    service = ProductService(product_repo)
    return service, product_repo


@pytest.fixture
def user_service_mock():
    user_repo = AsyncMock()
    service = UserService(user_repo)
    return service, user_repo


@pytest.fixture
def password_service():
    return PasswordService()


@pytest.fixture
def jwt_service():
    return JwtService()
