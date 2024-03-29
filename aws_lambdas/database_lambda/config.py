from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_URL: str
    ELASTIC_SEARCH_URL: str

    model_config = SettingsConfigDict(env_file=".database.env", env_file_encoding="utf-8")


setting = Config()  # type: ignore
