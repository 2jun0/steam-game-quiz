from typing import Any

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import Envrionment


class Config(BaseSettings):
    DATABASE_URL: MySQLDsn | str
    # ELASTIC_SEARCH_URL: str
    ENVIRONMENT: Envrionment = Envrionment.PRODUCTION

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Config()  # type: ignore
app_configs: dict[str, Any] = {"title": "API"}
