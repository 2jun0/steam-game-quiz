from sqlalchemy_utils import database_exists, drop_database

from src.config import Config

config = Config()  # type: ignore

if database_exists(config.DATABASE_URL):
    drop_database(config.DATABASE_URL)
