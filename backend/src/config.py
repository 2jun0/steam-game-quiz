from typing import Any

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings

from .constants import Envrionment


class Config(BaseSettings):
    DATABASE_URL: MySQLDsn | str

    ENVIRONMENT: Envrionment = Envrionment.PRODUCTION


settings = Config()  # type: ignore
app_configs: dict[str, Any] = {"title": "API"}
