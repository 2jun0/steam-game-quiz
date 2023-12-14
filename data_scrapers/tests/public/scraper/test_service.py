from typing import Any, Collection, Optional

from sqlalchemy.orm import Session

from public.model import (
    Game,
    GameScreenshot,
    SteamFeatureGameResponse,
    SteamGameDetailResponse,
    SteamGameScreenshotResponse,
)
from public.protocols import LambdaAPI, SteamAPI
from public.scraper.service import scrap_game_screenshot, scrap_games
from tests.public.factories import (
    GameFactory,
    SteamFeatureGameResponseFactory,
    SteamGameDetailResponseFactory,
    SteamGameScreenshotResponseFactory,
)


class MockSteamAPI(SteamAPI):
    def __init__(self):
        SteamFeatureGameResponseFactory.reset_sequence()
        SteamGameDetailResponseFactory.reset_sequence()
        SteamGameScreenshotResponseFactory.reset_sequence()

    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        return SteamFeatureGameResponseFactory.build_batch(100)

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        return SteamGameDetailResponseFactory.build()

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        return SteamGameScreenshotResponseFactory.build_batch(10)


class MockLambdaAPI(LambdaAPI):
    def __init__(self):
        GameFactory.reset_sequence()
        self.saved: list[Any] = []

    def get_some_games(self) -> list[Game]:
        return self.saved

    def get_games_in_steam_ids(self, steam_ids: Collection[int]) -> list[Game]:
        return self.saved

    def get_screenshots_in_steam_file_ids(self, steam_file_ids: Collection[int]) -> list[GameScreenshot]:
        return self.saved

    def save_games(self, games: Collection[Any]):
        self.saved.extend(games)

    def save_screenshots(self, screenshots: Collection[Any]):
        self.saved.extend(screenshots)


def test_scrap_geams는_새_게임을_저장한다():
    lambda_api = MockLambdaAPI()
    scrap_games(MockSteamAPI(), lambda_api)

    assert len(lambda_api.saved) > 0


def test_scrap_games는_중복된_게임은_다시_저장하지_않는다():
    lambda_api = MockLambdaAPI()
    scrap_games(MockSteamAPI(), lambda_api)
    before_scraped = len(lambda_api.saved)

    # duplicated games
    scrap_games(MockSteamAPI(), lambda_api)
    after_scraped = len(lambda_api.saved)

    assert before_scraped == after_scraped


def test_scrap_screenshots은_스크린샷을_저장한다(game: Game):
    lambda_api = MockLambdaAPI()
    scrap_game_screenshot(MockSteamAPI(), lambda_api, game)

    assert len(lambda_api.saved) > 0


def test_scrap_screenshot은_중복된_스크린샷은_다시_저장하지_않는다(session: Session, game: Game):
    lambda_api = MockLambdaAPI()
    scrap_game_screenshot(MockSteamAPI(), lambda_api, game)
    before_scraped = len(lambda_api.saved)

    # duplicated screenshots
    scrap_game_screenshot(MockSteamAPI(), lambda_api, game)
    after_scraped = len(lambda_api.saved)

    assert before_scraped == after_scraped
