import pytest

from src.database.models import Product


@pytest.fixture
def product():
    return Product(id=1, name="Product 1", price=100.0, stock=100)


@pytest.fixture
def products():
    return [
        Product(id=1, name="Product 1", price=100.0, stock=100),
        Product(id=2, name="Product 2", price=200.0, stock=200),
    ]
