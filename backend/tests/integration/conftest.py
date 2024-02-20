from typing import Any, Generator

import pytest
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session

from src.auth.dependency import current_active_user
from src.auth.model import User
from src.config import settings
from src.main import app
from tests.database import engine
from tests.utils.auth import create_random_user
from tests.utils.database import create_all_table, drop_tables
from tests.utils.es import create_all_indexes, delete_all_indexes


@pytest.fixture()
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


@pytest.fixture()
def current_user(session: Session) -> Generator[User, Any, None]:
    user = create_random_user(session, email="email@example.com")

    def override_current_active_user() -> User:
        return user

    app.dependency_overrides[current_active_user] = override_current_active_user
    yield user
    del app.dependency_overrides[current_active_user]


@pytest.fixture()
def es_client() -> Generator[Elasticsearch, Any, None]:
    es_client = Elasticsearch(settings.ELASTIC_SEARCH_URL)
    delete_all_indexes(es_client)
    create_all_indexes(es_client)
    yield es_client
    delete_all_indexes(es_client)
    es_client.close()
