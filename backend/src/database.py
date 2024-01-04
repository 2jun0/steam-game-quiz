from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from .config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)  # type: ignore


def create_all_table():
    SQLModel.metadata.create_all(engine.sync_engine)
