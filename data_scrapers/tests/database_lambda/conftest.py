from typing import Any, Generator

import pytest
from sqlalchemy.orm import Session

from tests.database_lambda.database import create_tables, drop_tables, engine, init_database


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
