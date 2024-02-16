from collections.abc import AsyncGenerator
from typing import Annotated, Any

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .database import engine
from .es import es_client as es_client_


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def es_client() -> AsyncGenerator[AsyncElasticsearch, Any]:
    yield es_client_
    await es_client_.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
