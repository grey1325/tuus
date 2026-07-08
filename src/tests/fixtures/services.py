from unittest.mock import AsyncMock
import pytest

from src.services.order_service import OrderService


@pytest.fixture
def order_service_mocks():
    order_repo = AsyncMock()
    user_repo = AsyncMock()
    product_repo = AsyncMock()
    service = OrderService(order_repo, user_repo, product_repo)
    return service, order_repo, user_repo, product_repo
