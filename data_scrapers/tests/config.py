from pydantic_settings import SettingsConfigDict

from src.config import Config


class TestConfig(Config):
    model_config = SettingsConfigDict(env_file=".test.env", env_file_encoding="utf-8")
