from sqlalchemy import Table, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from private.config import setting
from private.model import Base

engine = create_engine(setting.DATABASE_URL, echo=True)  # type: ignore
Session = scoped_session(sessionmaker(engine))


def get_tables() -> list[Table]:
    return list(Base.metadata.tables.values())


def init_database():
    if not database_exists(setting.DATABASE_URL):
        create_database(setting.DATABASE_URL)

    Base.metadata.create_all(engine, get_tables(), checkfirst=True)


def drop_tables():
    Base.metadata.drop_all(engine)
