from datetime import datetime
from decimal import Decimal

from src.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from src.dependencies import get_auth_service
from src.api.main import app


class FakeAuthService:

    async def register_user(self, user_create):
        return {
            "id": 1,
            "name": user_create.name,
            "email": user_create.email,
            "balance": Decimal("0.0"),
            "created_at": datetime.now(),
        }

    async def authenticate_user(self, user_login):
        return {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token",
            "token_type": "bearer",
        }

    async def refresh_access_token(self, refresh_token):
        return {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token",
            "token_type": "bearer",
        }


def override_auth_service():
    return FakeAuthService()


class FakeAuthAlreadyExistsService:

    async def register_user(self, user_create):
        raise UserAlreadyExistsError("User with this email already exists")


def override_auth_service_already_exists():
    return FakeAuthAlreadyExistsService()


class FakeInvalidCredentialsService:

    async def authenticate_user(self, user_login):
        raise InvalidCredentialsError("Invalid credentials")


def override_auth_service_invalid_credentials():
    return FakeInvalidCredentialsService()


class FakeInvalidRefreshTokenService:

    async def refresh_access_token(self, refresh_token):
        raise InvalidCredentialsError("Unexpected token type")


def override_auth_service_invalid_refresh_token():
    return FakeInvalidRefreshTokenService()


class FakeExpiredRefreshTokenService:

    async def refresh_access_token(self, refresh_token):
        raise InvalidCredentialsError("Token has expired")


def override_auth_service_expired_refresh_token():
    return FakeExpiredRefreshTokenService()


def test_register_user_success(client):
    app.dependency_overrides[get_auth_service] = override_auth_service

    response = client.post(
        "/auth/register",
        json={
            "name": "Ivan",
            "email": "new@example.com",
            "password": "password",
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["name"] == "Ivan"
    assert data["email"] == "new@example.com"
    assert data["balance"] == 0.0
    assert "created_at" in data


def test_register_user_already_exists(client):
    app.dependency_overrides[get_auth_service] = override_auth_service_already_exists

    response = client.post(
        "/auth/register",
        json={
            "name": "Ivan",
            "email": "new@example.com",
            "password": "password",
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}


def test_login_success(client):
    app.dependency_overrides[get_auth_service] = override_auth_service

    response = client.post(
        "/auth/login", json={"email": "new@example.com", "password": "password"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
        "token_type": "bearer",
    }


def test_login_invalid_credentials(client):
    app.dependency_overrides[get_auth_service] = (
        override_auth_service_invalid_credentials
    )

    response = client.post(
        "/auth/login", json={"email": "new@example.com", "password": "password"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_refresh_success(client):
    app.dependency_overrides[get_auth_service] = override_auth_service

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "fake_refresh_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
        "token_type": "bearer",
    }


def test_refresh_invalid_token(client):
    app.dependency_overrides[get_auth_service] = (
        override_auth_service_invalid_refresh_token
    )

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "fake_refresh_token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Unexpected token type"}


def test_refresh_expired_token(client):
    app.dependency_overrides[get_auth_service] = (
        override_auth_service_expired_refresh_token
    )

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "fake_refresh_token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Token has expired"}
