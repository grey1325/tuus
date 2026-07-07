from fastapi.testclient import TestClient
from src.api.main import app
from src.dependencies import get_product_service


class FakeProductService:
    async def get_products(self, skip: int = 0, limit: int = 100):
        return [
            {
                "id": 1,
                "name": "Phone",
                "price": 100.0,
                "stock": 10,
            }
        ]

    async def get_product(self, product_id: int):
        return {
            "id": 1,
            "name": "Phone",
            "price": 100.0,
            "stock": 10,
        }

    async def create_product(self, product):
        return {
            "id": 1,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "category": product.category,
        }

    async def update_product(self, product_id, product):
        return {
            "id": 1,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        }

    async def delete_product(self, product_id):
        return {"id": product_id}


class FakeProductNotFoundService:
    async def get_product(self, product_id: int):
        raise ValueError("Товар не найден")

    async def update_product(self, product_id, product):
        raise ValueError("Товар не найден")


def override_product_service():
    return FakeProductService()


def override_product_service_not_found():
    return FakeProductNotFoundService()


app.dependency_overrides[get_product_service] = override_product_service

client = TestClient(app)


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Phone", "price": 100.0, "stock": 10}]


def test_get_product_success():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Phone", "price": 100.0, "stock": 10}


def test_get_product_not_found():
    app.dependency_overrides[get_product_service] = override_product_service_not_found
    try:
        response = client.get("/products/99999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Товар не найден"}
    finally:
        app.dependency_overrides.clear()
    app.dependency_overrides[get_product_service] = override_product_service


def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "Phone", "price": 100.0, "stock": 10, "category": "Phone"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Phone",
        "price": 100.0,
        "stock": 10,
        "category": "Phone",
    }


def test_update_product_succes():
    response = client.put(
        "/products/1", json={"name": "Phone", "price": 100.0, "stock": 10}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Phone", "price": 100.0, "stock": 10}


def test_update_product_not_found():
    app.dependency_overrides[get_product_service] = override_product_service_not_found
    try:
        response = client.put(
            "/products/99999",
            json={"name": "Phone", "price": 100.0, "stock": 10},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Товар не найден"}
    finally:
        app.dependency_overrides.clear()
    app.dependency_overrides[get_product_service] = override_product_service


def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.json() == {"message": f"Товар {1} удалён"}
