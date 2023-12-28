from sqlmodel import SQLModel

from src.database import engine


def drop_tables():
    SQLModel.metadata.drop_all(engine)
