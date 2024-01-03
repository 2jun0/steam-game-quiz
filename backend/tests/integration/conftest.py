from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.database import engine
from src.main import app
from tests.utils.database import drop_tables


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_database():
    yield
    drop_tables()


@pytest.fixture()
def session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
