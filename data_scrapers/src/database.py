from sqlalchemy import Engine, Table
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from .config import Config
from .model import Base


def get_tables() -> list[Table]:
    return list(Base.metadata.tables.values())


def init_database(config: Config, engine: Engine):
    if not database_exists(config.DATABASE_URL):
        create_database(config.DATABASE_URL)

    Base.metadata.create_all(engine, get_tables(), checkfirst=True)
