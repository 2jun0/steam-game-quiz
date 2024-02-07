from daily_quiz.protocols import SteamAPI
from daily_quiz.steam.model import SteamGameScreenshotResponse

from ..utils.steam import create_random_screenshot

MOCK_GAME_SIZE = 100
FEATURE_GAME_SIZE = 100
MOCK_GENRE_SIZE = 10
MOCK_SCREENSHOT_SIZE = 1000
SCREENSHOT_PAGE_SIZE = 100


class MockSteamAPI(SteamAPI):
    def __init__(self) -> None:
        self.screenshots: dict[int, list[dict]] = {}

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        if app_id not in self.screenshots:
            self.screenshots[app_id] = [create_random_screenshot() for _ in range(100)]

        return [
            SteamGameScreenshotResponse(file_id=s["file_id"], full_image_url=s["url"])
            for s in self.screenshots[app_id][SCREENSHOT_PAGE_SIZE * (page - 1) : SCREENSHOT_PAGE_SIZE * page]
        ]
