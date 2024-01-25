from typing import Optional

from .. import protocols
from . import gamalytic_api, steampowered_api
from .model import (
    GamalyticSteamGameDetailResponse,
    SteamFeatureGameResponse,
    SteamGameDetailResponse,
    SteamGameScreenshotResponse,
)


class SteamAPI(protocols.SteamAPI):
    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        games = steampowered_api.get_feature_games()
        return [SteamFeatureGameResponse(app_id=game["id"], name=game["name"]) for game in games]

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        details = steampowered_api.get_app_details(app_id, language)
        return SteamGameDetailResponse(name=details["name"])

    def get_game_details_from_gamalytic(self, app_id: int) -> GamalyticSteamGameDetailResponse:
        details = gamalytic_api.get_game_details(app_id)

        return GamalyticSteamGameDetailResponse(
            name=details["name"], genres=details["genres"], released_at=details["releaseDate"] / 1000
        )

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        screenshots = steampowered_api.get_community_screenshots(app_id, page)

        return [
            SteamGameScreenshotResponse(
                file_id=int(screenshot["published_file_id"]), full_image_url=screenshot["full_image_url"]
            )
            for screenshot in screenshots
        ]
