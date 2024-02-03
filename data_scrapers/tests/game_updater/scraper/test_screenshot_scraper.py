import pytest

from game_updater.scraper.screenshot import scrap_game_screenshot
from tests.game_updater.utils.mock_lambda_api import MockLambdaAPI
from tests.game_updater.utils.mock_steam_api import MockSteamAPI
from tests.game_updater.utils.model import create_random_game


@pytest.fixture
def mock_steam_api() -> MockSteamAPI:
    return MockSteamAPI()


def test_scrap_screenshots은_스크린샷을_저장한다(mock_steam_api: MockSteamAPI):
    mock_steam_api.prepare_mock_data(game_size=1, screenshot_size=1)
    saved_game = list(mock_steam_api.games.values())[0]
    game = create_random_game(steam_id=saved_game["steam_id"], name=saved_game["name"])
    lambda_api = MockLambdaAPI()

    scrap_game_screenshot(mock_steam_api, lambda_api, game)

    assert len(lambda_api.screenshots.values()) > 0


def test_scrap_screenshot은_중복된_스크린샷은_다시_저장하지_않는다(mock_steam_api: MockSteamAPI):
    mock_steam_api.prepare_mock_data(game_size=1, screenshot_size=1)
    saved_game = list(mock_steam_api.games.values())[0]
    game = create_random_game(steam_id=saved_game["steam_id"], name=saved_game["name"])
    lambda_api = MockLambdaAPI()

    scrap_game_screenshot(mock_steam_api, lambda_api, game)
    before_scraped = lambda_api.screenshots.copy()

    # duplicated screenshots
    scrap_game_screenshot(mock_steam_api, lambda_api, game)
    after_scraped = lambda_api.screenshots

    assert before_scraped == after_scraped
