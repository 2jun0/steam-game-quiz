from collections.abc import Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_LAMBDA_NAME: str = "database"
    DAILY_QUIZ_CNT: int = 5
    GAME_GENERES: Sequence[str] = [
        "Action",
        "Adventure",
        "Massively Multiplayer",
        "Strategy",
        "RPG",
        "Indie",
        "Simulation",
        "Casual",
        "Racing",
        "Sports",
    ]
    OLDER_GAME_COUNT: int = 2  # Newer game count will be `DAILY_QUIZ_CNT` - `OLDER_GAME_COUNT`

    model_config = SettingsConfigDict(env_file=".daily_quiz.env", env_file_encoding="utf-8")


setting = Config()  # type: ignore
