from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict()


setting = Config()  # type: ignore
