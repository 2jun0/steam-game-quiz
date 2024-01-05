from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session

from src.main import app
from tests.database import engine
from tests.utils.database import create_all_table, drop_tables


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def database():
    create_all_table()
    yield
    drop_tables()


@pytest.fixture()
def session(database: Engine) -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
