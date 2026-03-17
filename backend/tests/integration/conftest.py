import asyncio
from typing import AsyncGenerator

import pytest
from meilisearch_python_sdk import AsyncClient
from httpx import AsyncClient as HttpxClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependency import current_active_user
from src.auth.model import User
from src.config import settings
from src.dependency import ms_client as ms_client_
from src.main import app
from tests.database import engine
from tests.utils.auth import create_random_user
from tests.utils.database import create_all_table, drop_tables
from tests.utils.es import create_all_indexes, delete_all_indexes

lock = asyncio.Lock()


@pytest.fixture(autouse=True)
async def database():
    async with lock:
        await drop_tables()
        await create_all_table()
        yield
        await drop_tables()


@pytest.fixture()
async def client() -> AsyncGenerator[HttpxClient, None]:
    async with HttpxClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture()
async def session(database) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture()
async def current_user(session: AsyncSession) -> AsyncGenerator[User, None]:
    user = await create_random_user(session, email="email@example.com")

    def override_current_active_user() -> User:
        return user

    app.dependency_overrides[current_active_user] = override_current_active_user
    yield user
    del app.dependency_overrides[current_active_user]


@pytest.fixture()
async def ms_client() -> AsyncGenerator[AsyncClient, None]:
    client = AsyncClient(settings.MEILISEARCH_URL)

    def override_ms_client() -> AsyncClient:
        return client

    await delete_all_indexes(client)
    await create_all_indexes(client)

    app.dependency_overrides[ms_client_] = override_ms_client
    yield client
    await delete_all_indexes(client)
    await client.aclose()
