import pytest

from public.scraper.service import scrap_game_screenshot, scrap_games
from tests.public.utils.mock_lambda_api import MockLambdaAPI
from tests.public.utils.mock_steam_api import MockSteamAPI
from tests.public.utils.model import create_random_game


@pytest.fixture
def mock_steam_api() -> MockSteamAPI:
    return MockSteamAPI()


def test_scrap_geams는_새_게임을_저장한다(mock_steam_api: MockSteamAPI):
    mock_steam_api.prepare_mock_data()
    lambda_api = MockLambdaAPI()

    scrap_games(mock_steam_api, lambda_api)

    assert len(lambda_api.games.values()) > 0


def test_scrap_games는_중복된_게임은_다시_저장하지_않는다(mock_steam_api: MockSteamAPI):
    mock_steam_api.prepare_mock_data()
    lambda_api = MockLambdaAPI()

    scrap_games(mock_steam_api, lambda_api)
    before_scraped = lambda_api.games.copy()

    # duplicated games
    scrap_games(mock_steam_api, lambda_api)
    after_scraped = lambda_api.games

    assert before_scraped == after_scraped


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
