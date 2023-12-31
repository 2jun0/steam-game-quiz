from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from sqlmodel import Session

from src.database import engine
from src.main import app
from tests.utils.database import drop_tables


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", "9000"
    scope = {"client": {host, port}}

    async with TestClient(app, scope=scope) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def clear_database():
    yield
    drop_tables()


@pytest.fixture()
def session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
