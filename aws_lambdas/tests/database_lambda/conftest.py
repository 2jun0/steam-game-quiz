from typing import Any, Generator

import pytest
from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from tests.database_lambda.database import create_tables, drop_tables, engine, init_database
from tests.database_lambda.es import create_all_indexes, delete_all_indexes
from tests.database_lambda.es import es_client as _es_client


@pytest.fixture(autouse=True)
def database():
    init_database()
    create_tables()
    yield
    drop_tables()


@pytest.fixture
def session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture
def es_client() -> Generator[Elasticsearch, Any, None]:
    delete_all_indexes(_es_client)
    create_all_indexes(_es_client)
    yield _es_client
    delete_all_indexes(_es_client)
