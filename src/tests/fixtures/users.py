import pytest
from src.api.schemas import UserUpdate
from src.database.models import User


@pytest.fixture
def user():
    return User(id=1, name="Ivan", email="new@example.com")


@pytest.fixture
def users():
    return [
        User(id=1, name="Ivan", email="new@example.com"),
        User(id=2, name="Ivan", email="new_2@example.com"),
    ]


@pytest.fixture
def user_update():
    return UserUpdate(name="Ivan", email="new_3@example.com")
