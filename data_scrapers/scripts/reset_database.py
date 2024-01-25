import pathlib
import sys

from sqlalchemy_utils import create_database, database_exists, drop_database

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import private.genre.model  # noqa: E402, F401
import private.screenshot.model  # noqa: E402, F401
from private.config import setting  # noqa: E402
from private.database import Base, engine  # noqa: E402
from private.game.model import game_genre_link  # noqa: E402

if database_exists(setting.DATABASE_URL):
    drop_database(setting.DATABASE_URL)


create_database(setting.DATABASE_URL)

tables = list(Base.metadata.tables.values()) + [game_genre_link]
Base.metadata.create_all(engine, tables, checkfirst=True)
