from fastapi.testclient import TestClient
import pytest
from src.api.main import app


@pytest.fixture()
def client():
    test_client = TestClient(app)
    yield test_client
