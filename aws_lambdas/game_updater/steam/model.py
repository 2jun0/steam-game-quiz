from typing import Sequence

from pydantic import BaseModel


class SteamGameDetailResponse(BaseModel):
    name: str


class GamalyticSteamGameResponse(BaseModel):
    app_id: int
    name: str
    genres: Sequence[str]
    released_at: float
    copies_sold: int


class SteamFeatureGameResponse(BaseModel):
    app_id: int
    name: str


class SteamGameScreenshotResponse(BaseModel):
    file_id: int
    full_image_url: str
