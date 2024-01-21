from sqlalchemy import Table, create_engine
from sqlalchemy_utils import create_database, database_exists

from .config import setting
from .model import Base

engine = create_engine(setting.DATABASE_URL)


def get_tables() -> list[Table]:
    return list(Base.metadata.tables.values())


def init_database():
    if not database_exists(setting.DATABASE_URL):
        create_database(setting.DATABASE_URL)

    Base.metadata.create_all(engine, get_tables(), checkfirst=True)
