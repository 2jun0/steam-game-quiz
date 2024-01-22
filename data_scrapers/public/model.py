from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel, Field


class Game(BaseModel):
    id: int
    steam_id: int
    name: str
    kr_name: Optional[str]
    owners: int
    genres: list[str]
    updated_at: datetime
    created_at: datetime


class GameScreenshot(BaseModel):
    id: int
    steam_file_id: int
    url: str = Field(max_length=2048)
    game_id: int
    game: Game = Field(repr=False)
    updated_at: datetime
    created_at: datetime


class NewGame(BaseModel):
    steam_id: int
    name: Optional[str]
    kr_name: Optional[str] = Field(default=None)
    owners: Optional[int] = Field(default=None)
    genres: Optional[Sequence[str]] = Field(default=[])


class NewGameScreenshot(BaseModel):
    steam_file_id: int
    url: str = Field(max_length=2048)
    game_id: int


class SteamGameDetailResponse(BaseModel):
    name: str


class GamalyticSteamGameDetailResponse(BaseModel):
    name: str
    genres: Sequence[str]
    owners: int


class SteamFeatureGameResponse(BaseModel):
    app_id: int
    name: str


class SteamGameScreenshotResponse(BaseModel):
    file_id: int
    full_image_url: str
