from src.dependencies import get_order_service
from src.api.main import app


class FakeOrderService:

    async def get_orders(self, skip: int, limit: int):
        return [
            {
                "id": 1,
                "user_id": 1,
                "total": 1000,
                "status": "pending",
                "order_date": "2021-01-01T00:00:00",
                "items": [
                    {"product": {"id": 1, "name": "Phone", "price": 100}, "quantity": 1}
                ],
            }
        ]

    async def get_order(self, order_id: int):
        return {
            "id": order_id,
            "user_id": 1,
            "total": 1000,
            "status": "pending",
            "order_date": "2021-01-01T00:00:00",
            "items": [
                {"product": {"id": 1, "name": "Phone", "price": 100}, "quantity": 1}
            ],
        }

    async def create_order(self, order_data):
        return {
            "id": 1,
            "user_id": 1,
            "total": 1000,
            "status": "pending",
            "order_date": "2021-01-01T00:00:00",
            "items": [
                {"product": {"id": 1, "name": "Phone", "price": 100}, "quantity": 1}
            ],
        }

    async def update_status(self, order_id, order_update):
        return {
            "id": order_id,
            "user_id": 1,
            "total": 1000,
            "status": "pending",
            "order_date": "2021-01-01T00:00:00",
            "items": [
                {"product": {"id": 1, "name": "Phone", "price": 100}, "quantity": 1}
            ],
        }


class FakeOrderNotFoundService:
    async def get_order(self, order_id: int):
        raise ValueError(f"Заказ {order_id} не найден")

    async def update_status(self, order_id, order_update):
        raise ValueError(f"Заказ {order_id} не найден")


def override_order_service():
    return FakeOrderService()


def override_order_service_not_found():
    return FakeOrderNotFoundService()


def test_get_orders(client):
    app.dependency_overrides[get_order_service] = override_order_service
    response = client.get("/orders/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "user_id": 1,
            "total": 1000,
            "status": "pending",
            "order_date": "2021-01-01T00:00:00",
            "items": [
                {"product": {"id": 1, "name": "Phone", "price": 100}, "quantity": 1}
            ],
        }
    ]


def test_get_order_success(client):
    app.dependency_overrides[get_order_service] = override_order_service
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "total": 1000,
        "status": "pending",
        "order_date": "2021-01-01T00:00:00",
        "items": [{"product": {"id": 1, "name": "Phone", "price": 100}, "quantity": 1}],
    }


def test_get_order_not_found(client):
    app.dependency_overrides[get_order_service] = override_order_service_not_found
    response = client.get("/orders/1")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Заказ {1} не найден"}


def test_create_order(client):
    app.dependency_overrides[get_order_service] = override_order_service
    response = client.post(
        "/orders/",
        json={
            "user_id": 1,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 1,
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "total": 1000,
        "status": "pending",
        "order_date": "2021-01-01T00:00:00",
        "items": [
            {
                "product": {
                    "id": 1,
                    "name": "Phone",
                    "price": 100,
                },
                "quantity": 1,
            }
        ],
    }


def test_update_status_success(client):
    app.dependency_overrides[get_order_service] = override_order_service
    response = client.patch("/orders/1/status", json={"status": "paid"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "total": 1000,
        "status": "pending",
        "order_date": "2021-01-01T00:00:00",
        "items": [
            {
                "product": {
                    "id": 1,
                    "name": "Phone",
                    "price": 100,
                },
                "quantity": 1,
            }
        ],
    }


def test_update_status_not_found(client):
    app.dependency_overrides[get_order_service] = override_order_service_not_found
    response = client.patch("/orders/1/status", json={"status": "paid"})
    assert response.status_code == 404
    assert response.json() == {"detail": f"Заказ {1} не найден"}
