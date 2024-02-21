from datetime import date, datetime
from typing import Optional, Sequence

from pydantic import BaseModel, field_serializer


class Game(BaseModel):
    id: int
    steam_id: int
    name: str
    kr_name: Optional[str]
    released_at: datetime
    genres: Sequence[str]
    updated_at: datetime
    created_at: datetime

    def __hash__(self) -> int:
        return hash(self.id)


class SaveGameScreenshot(BaseModel):
    steam_file_id: int
    url: str
    game_id: int


class SaveQuiz(BaseModel):
    screenshots: Sequence[SaveGameScreenshot]


class SaveDailyQuiz(BaseModel):
    quiz: SaveQuiz
    target_date: date
    feature: str

    @field_serializer("target_date")
    def serialize_target_date(self, target_date: date, _info) -> str:
        return str(target_date)
