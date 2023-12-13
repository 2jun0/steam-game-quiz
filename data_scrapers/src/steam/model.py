from dataclasses import dataclass


@dataclass
class SteamGameDetailResponse:
    name: str


@dataclass
class SteamFeatureGameResponse:
    app_id: int
    name: str


@dataclass
class SteamGameScreenshotResponse:
    file_id: int
    full_image_url: int
