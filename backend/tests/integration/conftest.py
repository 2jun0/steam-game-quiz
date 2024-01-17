from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session

from src.auth.dependency import current_active_user
from src.main import app
from tests.database import engine
from tests.utils.auth import create_random_user
from tests.utils.database import create_all_table, drop_tables


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def database():
    drop_tables()
    create_all_table()
    yield
    drop_tables()


@pytest.fixture()
def session(database: Engine) -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


"""override dependencies"""


@pytest.fixture(autouse=True)
def override_dependencies(session: Session):
    def override_current_active_user():
        return create_random_user(session, email="email@example.com")

    app.dependency_overrides[current_active_user] = override_current_active_user
