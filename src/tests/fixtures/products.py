import pytest

from src.api.schemas import ProductUpdate
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


@pytest.fixture
def product_update():
    return ProductUpdate(
        name="New Product",
        price=150.0,
        stock=20,
    )
