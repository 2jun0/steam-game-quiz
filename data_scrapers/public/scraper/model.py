from typing import Optional, Sequence

from pydantic import BaseModel, Field


class NewGame(BaseModel):
    steam_id: int
    name: Optional[str]
    kr_name: Optional[str] = Field(default=None)
    released_at: Optional[float] = Field(default=None)
    genres: Optional[Sequence[str]] = Field(default=[])


class NewGameScreenshot(BaseModel):
    steam_file_id: int
    url: str = Field(max_length=2048)
    game_id: int
