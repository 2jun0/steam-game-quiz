from typing import Optional, Protocol, Sequence

from .aws_lambda.model import Game, GameScreenshot, SaveGame
from .scraper.model import NewGameScreenshot
from .steam.model import (
    GamalyticSteamGameDetailResponse,
    GamalyticSteamGameResponse,
    SteamFeatureGameResponse,
    SteamGameDetailResponse,
    SteamGameScreenshotResponse,
)


class SteamAPI(Protocol):
    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        ...

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        ...

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        ...

    def get_game_details_from_gamalytic(self, app_id: int) -> GamalyticSteamGameDetailResponse:
        ...

    def get_all_games_from_gamalytic(self, worker_cnt: int) -> list[GamalyticSteamGameResponse]:
        ...


class LambdaAPI(Protocol):
    def get_some_games(self) -> list[Game]:
        ...

    def get_games_in_steam_ids(self, steam_ids: Sequence[int]) -> list[Game]:
        ...

    def get_screenshots_in_steam_file_ids(self, steam_file_ids: Sequence[int]) -> list[GameScreenshot]:
        ...

    def save_games(self, games: Sequence[SaveGame]):
        ...

    def save_screenshots(self, screenshots: Sequence[NewGameScreenshot]):
        ...
