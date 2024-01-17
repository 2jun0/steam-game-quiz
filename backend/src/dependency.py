from typing import Annotated, Any, AsyncGenerator

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings
from .database import engine


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def es_client() -> AsyncElasticsearch:
    return AsyncElasticsearch(settings.ELASTIC_SEARCH_URL)  # type: ignore


SessionDep = Annotated[AsyncSession, Depends(get_session)]
