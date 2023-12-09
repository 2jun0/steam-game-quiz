from typing import Optional, Protocol

from ..steam.model import SteamGameDetailResponse, SteamGameScreenshotResponse, TopSteamGameResponse


class SteamAPI(Protocol):
    def get_top_100_games_in_2weeks(self) -> list[TopSteamGameResponse]:
        ...

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        ...

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        ...
