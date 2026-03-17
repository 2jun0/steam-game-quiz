from typing import Any, Generator

import meilisearch
import pytest
from sqlalchemy.orm import Session

from tests.database_lambda.database import create_tables, drop_tables, engine, init_database
from tests.database_lambda.es import create_all_indexes, delete_all_indexes
from tests.database_lambda.es import ms_client as _ms_client


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
def ms_client() -> Generator[meilisearch.Client, Any, None]:
    delete_all_indexes(_ms_client)
    create_all_indexes(_ms_client)
    yield _ms_client
    delete_all_indexes(_ms_client)
