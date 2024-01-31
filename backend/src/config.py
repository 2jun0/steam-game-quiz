from typing import Any

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import Envrionment


class Config(BaseSettings):
    DATABASE_URL: MySQLDsn | str
    # ELASTIC_SEARCH_URL: str
    CORS_ORIGINS: list[str] = []

    # auth
    JWT_SECRET: str
    OAUTH2_SECRET: str
    GOOGLE_OAUTH2_CLIENT_ID: str
    GOOGLE_OAUTH2_CLIENT_SECRET: str
    GOOGLE_OAUTH2_REDIRECT_URL: str | None = None

    ENVIRONMENT: Envrionment = Envrionment.PRODUCTION

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Config()  # type: ignore
app_configs: dict[str, Any] = {"title": "API"}
