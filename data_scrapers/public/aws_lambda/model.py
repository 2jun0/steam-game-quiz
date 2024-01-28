from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel, Field


class Game(BaseModel):
    id: int
    steam_id: int
    name: str
    kr_name: Optional[str]
    released_at: datetime
    genres: Sequence[str]
    updated_at: datetime
    created_at: datetime


class GameScreenshot(BaseModel):
    id: int
    steam_file_id: int
    url: str
    game_id: int
    game: Game = Field(repr=False)
    updated_at: datetime
    created_at: datetime


class SaveGame(BaseModel):
    steam_id: int
    name: str
    kr_name: Optional[str]
    released_at: float
    genres: Sequence[str]