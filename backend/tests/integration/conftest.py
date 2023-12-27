from typing import AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

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
