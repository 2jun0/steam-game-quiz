from typing import Any, Generator

import pytest
from sqlalchemy.orm import Session

from tests.private.database import drop_tables, engine, init_database


@pytest.fixture(autouse=True)
def database():
    init_database()
    yield
    drop_tables()
    engine.dispose()


@pytest.fixture
def session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
