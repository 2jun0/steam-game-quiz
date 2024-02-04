from typing import Optional, Protocol, Sequence

from .aws_lambda.model import SaveGame
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
    def save_games(self, games: Sequence[SaveGame]):
        ...
