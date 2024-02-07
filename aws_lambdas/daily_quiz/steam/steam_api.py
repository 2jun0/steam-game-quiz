from .. import protocols
from . import steampowered_api
from .model import SteamGameScreenshotResponse


class SteamAPI(protocols.SteamAPI):
    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        screenshots = steampowered_api.get_community_screenshots(app_id, page)

        return [
            SteamGameScreenshotResponse(
                file_id=int(screenshot["published_file_id"]), full_image_url=screenshot["full_image_url"]
            )
            for screenshot in screenshots
        ]
