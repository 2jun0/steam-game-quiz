import asyncio
from typing import AsyncGenerator

import pytest
from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependency import current_active_user
from src.auth.model import User
from src.config import settings
from src.dependency import es_client as es_client_
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
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
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
async def es_client() -> AsyncGenerator[AsyncElasticsearch, None]:
    es_client = AsyncElasticsearch(settings.ELASTIC_SEARCH_URL)

    def override_es_client() -> AsyncElasticsearch:
        return es_client

    await delete_all_indexes(es_client)
    await create_all_indexes(es_client)

    app.dependency_overrides[es_client_] = override_es_client
    yield es_client
    await delete_all_indexes(es_client)
    await es_client.close()
