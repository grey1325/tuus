import pytest
from src.api.schemas import UserCreate, UserLogin, UserUpdate
from src.database.models import User


@pytest.fixture
def user():
    return User(id=1, name="Ivan", email="new@example.com", password_hash="password")


@pytest.fixture
def users():
    return [
        User(id=1, name="Ivan", email="new@example.com", password_hash="password"),
        User(id=2, name="Ivan", email="new_2@example.com", password_hash="password"),
    ]


@pytest.fixture
def user_update():
    return UserUpdate(name="Ivan", email="new_3@example.com")


@pytest.fixture
def user_create():
    return UserCreate(name="Ivan", email="new@example.com", password="password")


@pytest.fixture
def user_login():
    return UserLogin(email="new@example.com", password="password")
