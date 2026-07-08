import pytest

from src.database.models import Order


@pytest.fixture
def order():
    return Order(id=1, user_id=1, total=100.0)


@pytest.fixture
def orders():
    return [
        Order(id=1, user_id=1, total=100.0),
        Order(id=2, user_id=2, total=200.0),
    ]
