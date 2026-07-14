from datetime import datetime
from decimal import Decimal

from src.database.models import User
from src.dependencies import get_current_user, get_user_service
from src.api.main import app


class FakeUserService:

    async def get_users(self, skip: int = 0, limit: int = 100):
        return [
            {
                "id": 1,
                "name": "Ivan",
                "email": "new@example.com",
                "balance": 1000,
                "created_at": "2026-01-01T00:00:00",
            }
        ]

    async def get_user(self, user_id: int):
        return {
            "id": 1,
            "name": "Ivan",
            "email": "new@example.com",
            "balance": 1000,
            "created_at": "2026-01-01T00:00:00",
        }

    async def create_user(self, user):
        return {
            "id": 1,
            "name": "Ivan",
            "email": "new@example.com",
            "balance": 1000,
            "created_at": "2026-01-01T00:00:00",
        }

    async def update_user(self, user_id, user_update):
        return {
            "name": "Ivan",
            "email": "new@example.com",
        }

    async def delete_user(self, user_id):
        return {"message": f"Пользователь {user_id} удалён"}


class FakeUserNotFoundService:
    async def get_user(self, user_id: int):
        raise ValueError(f"Пользователь {user_id} не найден")

    async def update_user(self, user_id, user_update):
        raise ValueError(f"Пользователь {user_id} не найден")


def override_user_service():
    return FakeUserService()


def override_user_service_not_found():
    return FakeUserNotFoundService()


def override_current_user():
    return User(
        id=1,
        name="Ivan",
        email="new@example.com",
        password_hash="password",
        balance=Decimal("1000"),
        created_at=datetime(2026, 1, 1),
    )


def test_get_users(client):
    app.dependency_overrides[get_user_service] = override_user_service
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Ivan",
            "email": "new@example.com",
            "balance": 1000,
            "created_at": "2026-01-01T00:00:00",
        }
    ]


def test_get_user_success(client):
    app.dependency_overrides[get_user_service] = override_user_service
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Ivan",
        "email": "new@example.com",
        "balance": 1000,
        "created_at": "2026-01-01T00:00:00",
    }


def test_get_user_not_found(client):
    app.dependency_overrides[get_user_service] = override_user_service_not_found
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь {99999} не найден"}


def test_update_user_success(client):
    app.dependency_overrides[get_user_service] = override_user_service
    response = client.put("/users/1", json={"name": "Ivan", "email": "new@example.com"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Ivan",
        "email": "new@example.com",
    }


def test_update_user_not_found(client):
    app.dependency_overrides[get_user_service] = override_user_service_not_found
    response = client.put(
        "/users/99999", json={"name": "Ivan", "email": "new@example.com"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь {99999} не найден"}


def test_delete_user(client):
    app.dependency_overrides[get_user_service] = override_user_service
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": f"Пользователь {1} удалён"}


def test_read_users_me(client):
    app.dependency_overrides[get_current_user] = override_current_user
    response = client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Ivan"
    assert data["email"] == "new@example.com"
    assert data["balance"] == 1000
