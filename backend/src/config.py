from typing import Any
from pydantic_settings import BaseSettings
from pydantic import MySQLDsn

from constants import Envrionment


class Config(BaseSettings):
    DATABASE_URL: MySQLDsn

    ENVIRONMENT: Envrionment = Envrionment.PRODUCTION


settings = Config()
app_configs: dict[str, Any] = {"title": "API"}
