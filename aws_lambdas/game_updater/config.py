from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    WORKER_CNT: int = 10
    MIN_REVENUE: int = 10000000  # 10M
    DATABASE_LAMBDA_NAME: str = "database"

    model_config = SettingsConfigDict(env_file=".scraper.env", env_file_encoding="utf-8")


setting = Config()  # type: ignore
