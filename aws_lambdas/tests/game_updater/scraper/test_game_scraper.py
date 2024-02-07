import pytest

from game_updater.config import setting
from game_updater.scraper.game import scrap_games
from tests.game_updater.utils.mock_lambda_api import MockLambdaAPI
from tests.game_updater.utils.mock_steam_api import MockSteamAPI
from tests.game_updater.utils.steam import create_random_game


@pytest.fixture
def mock_steam_api() -> MockSteamAPI:
    return MockSteamAPI()


def test_scrap_geams는_새_게임을_저장한다(mock_steam_api: MockSteamAPI):
    mock_steam_api.prepare_mock_data()
    lambda_api = MockLambdaAPI()

    scrap_games(mock_steam_api, lambda_api)

    assert len(lambda_api.games.values()) > 0


def test_scrap_geams는_수익이_높은_게임만_저장한다(mock_steam_api: MockSteamAPI):
    popular_game = create_random_game(revenue=setting.MIN_REVENUE, tags=[])
    unpopular_game = create_random_game(revenue=setting.MIN_REVENUE - 1, tags=[])
    mock_steam_api.add_mock_game(popular_game)
    mock_steam_api.add_mock_game(unpopular_game)
    lambda_api = MockLambdaAPI()

    scrap_games(mock_steam_api, lambda_api)

    saved = list(lambda_api.games.values())
    assert len(saved) == 1
    assert saved[0].steam_id == popular_game["steam_id"]


@pytest.mark.parametrize("sex_tag", ("Sexual Content", "NSFW"))
def test_scrap_geams는_성적인_게임을_저장하지_않는다(mock_steam_api: MockSteamAPI, sex_tag: str):
    sexual_game = create_random_game(revenue=setting.MIN_REVENUE, tags=[sex_tag])
    mock_steam_api.add_mock_game(sexual_game)
    lambda_api = MockLambdaAPI()

    scrap_games(mock_steam_api, lambda_api)

    saved = list(lambda_api.games.values())
    assert len(saved) == 0
