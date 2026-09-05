import os

import pytest
from fastapi.testclient import TestClient


os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://test:test@localhost:5432/test",
)

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
