from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel


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
