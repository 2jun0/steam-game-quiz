from typing import Optional, Protocol

from ..steam.model import SteamFeatureGameResponse, SteamGameDetailResponse, SteamGameScreenshotResponse


class SteamAPI(Protocol):
    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        ...

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        ...

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        ...
