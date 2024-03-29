from sqlalchemy import Table, create_engine
from sqlalchemy_utils import create_database, database_exists

import database_lambda.game.model  # noqa: F401
import database_lambda.genre.model  # noqa: F401
import database_lambda.screenshot.model  # noqa: F401
from database_lambda.config import setting
from database_lambda.model import Base

engine = create_engine(setting.DATABASE_URL, echo=True)  # type: ignore


def get_tables() -> list[Table]:
    return list(Base.metadata.tables.values())


def init_database():
    if not database_exists(setting.DATABASE_URL):
        create_database(setting.DATABASE_URL)


def create_tables():
    Base.metadata.create_all(engine, get_tables(), checkfirst=True)


def drop_tables():
    Base.metadata.drop_all(engine, get_tables())
