from typing import Collection, Optional, Protocol

from .aws_lambda.model import Game, GameScreenshot
from .scraper.model import NewGame, NewGameScreenshot
from .steam.model import (
    GamalyticSteamGameDetailResponse,
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


class LambdaAPI(Protocol):
    def get_some_games(self) -> list[Game]:
        ...

    def get_games_in_steam_ids(self, steam_ids: Collection[int]) -> list[Game]:
        ...

    def get_screenshots_in_steam_file_ids(self, steam_file_ids: Collection[int]) -> list[GameScreenshot]:
        ...

    def save_games(self, games: Collection[NewGame]):
        ...

    def save_screenshots(self, screenshots: Collection[NewGameScreenshot]):
        ...
