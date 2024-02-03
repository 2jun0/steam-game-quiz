import pathlib
import sys

from sqlalchemy_utils import create_database, database_exists, drop_database

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import database_lambda.genre.model  # noqa: E402, F401
import database_lambda.screenshot.model  # noqa: E402, F401
from database_lambda.config import setting  # noqa: E402
from database_lambda.database import Base, engine  # noqa: E402

if database_exists(setting.DATABASE_URL):
    drop_database(setting.DATABASE_URL)


create_database(setting.DATABASE_URL)

tables = list(Base.metadata.tables.values())
Base.metadata.create_all(engine, tables, checkfirst=True)
