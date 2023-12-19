from typing import Any
from pydantic_settings import BaseSetting
from pydantic import MySQLDsn

from constants import Envrionment


class Config(BaseSetting):
    DATABASE_URL: MySQLDsn

    ENVIRONMENT: Envrionment


app_configs: dict[str, Any] = {"title": "API"}
