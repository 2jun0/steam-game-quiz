from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
