from sqlmodel import SQLModel, create_engine

from .config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)


def create_all_table():
    SQLModel.metadata.create_all(engine)
