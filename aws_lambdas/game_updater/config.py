from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_LAMBDA_NAME: str = "database"

    WORKER_CNT: int = 10
    MIN_REVENUE: int = 10000000  # 10M

    IGDB_CLIENT_ID: str
    IGDB_CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file=".game_updater.env", env_file_encoding="utf-8")


setting = Config()  # type: ignore
