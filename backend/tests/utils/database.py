from sqlmodel import SQLModel

from tests.database import engine


def drop_tables():
    SQLModel.metadata.drop_all(engine)


def create_all_table():
    SQLModel.metadata.create_all(engine)
