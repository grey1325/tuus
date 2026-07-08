import pytest
from src.database.models import User


@pytest.fixture
def user():
    return User(id=1, name="Ivan", email="new@example.com")
