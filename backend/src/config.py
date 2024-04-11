from typing import Any

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import Envrionment


class Config(BaseSettings):
    DATABASE_URL: MySQLDsn | str
    ELASTIC_SEARCH_URL: str
    CORS_ORIGINS: list[str] = []

    QUIZ_ANSWER_SUBMISSION_LIMIT: int = 3

    # auth
    JWT_SECRET: str
    OAUTH2_SECRET: str
    GOOGLE_OAUTH2_CLIENT_ID: str
    GOOGLE_OAUTH2_CLIENT_SECRET: str
    GOOGLE_OAUTH2_REDIRECT_URL: str | None = None
    FACEBOOK_OAUTH2_CLIENT_ID: str
    FACEBOOK_OAUTH2_CLIENT_SECRET: str
    FACEBOOK_OAUTH2_REDIRECT_URL: str | None = None

    # score
    SCORE_DIFF_ON_CORRECT_FIRST: int = 10
    SCORE_DIFF_ON_CORRECT_REPEAT: int = 2
    SCORE_DIFF_ON_FAILED: int = -2
    SCORE_DIFF_ON_FAILED_AFTER_PREV_SOLVED: int = -5

    ENVIRONMENT: Envrionment = Envrionment.PRODUCTION

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Config()  # type: ignore

if settings.ENVIRONMENT == Envrionment.PRODUCTION:
    app_configs: dict[str, Any] = {"title": "SteamQuizGame API", "version": "1", "docs_url": None, "redoc_url": None}
else:
    app_configs: dict[str, Any] = {"title": "SteamQuizGame API", "version": "1"}
