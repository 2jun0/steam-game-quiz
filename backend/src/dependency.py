from collections.abc import AsyncGenerator
from typing import Annotated, Any

from meilisearch_python_sdk import AsyncClient
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .database import engine
from .es import ms_client as ms_client_


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.commit()


async def ms_client() -> AsyncGenerator[AsyncClient, Any]:
    yield ms_client_


SessionDep = Annotated[AsyncSession, Depends(get_session)]
MeilisearchClientDep = Annotated[AsyncClient, Depends(ms_client)]
