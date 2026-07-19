from decimal import Decimal
import pytest
from sqlalchemy import select

from src.database.models import Product


@pytest.mark.asyncio
async def test_get_products(async_client, db_session):
    product = Product(name="Product 1", price=Decimal("100"), stock=100)
    db_session.add(product)
    await db_session.flush()

    response = await async_client.get("/products/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

    assert data[0]["id"] == product.id
    assert data[0]["name"] == product.name
    assert data[0]["price"] == float(product.price)
    assert data[0]["stock"] == product.stock


@pytest.mark.asyncio
async def test_get_product(async_client, db_session):
    product = Product(name="Product 1", price=Decimal("100"), stock=100)
    db_session.add(product)
    await db_session.flush()

    response = await async_client.get(f"/products/{product.id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == product.id
    assert data["name"] == product.name
    assert data["price"] == float(product.price)
    assert data["stock"] == product.stock


@pytest.mark.asyncio
async def test_get_product_not_found(async_client, db_session):
    product_id = 99999
    response = await async_client.get(f"/products/{product_id}")

    assert response.status_code == 404

    data = response.json()
    assert data == {"detail": f"Товар {product_id} не найден"}


@pytest.mark.asyncio
async def test_create_product(async_client, db_session):
    payload = {"name": "Product 1", "price": 100, "stock": 100}

    response = await async_client.post("/products/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]

    query = select(Product).where(Product.id == data["id"])
    result = await db_session.execute(query)
    product = result.scalar_one_or_none()
    assert product is not None

    assert product.name == payload["name"]
    assert float(product.price) == payload["price"]
    assert product.stock == payload["stock"]


@pytest.mark.asyncio
async def test_create_product_without_name(async_client, db_session):
    payload = {
        "price": 100,
        "stock": 100,
    }

    response = await async_client.post("/products/", json=payload)

    assert response.status_code == 422

    data = response.json()
    error = data["detail"][0]

    assert error["loc"] == ["body", "name"]
    assert error["type"] == "missing"
