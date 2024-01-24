import pytest

from public.scraper.game import scrap_games
from tests.public.utils.mock_lambda_api import MockLambdaAPI
from tests.public.utils.mock_steam_api import MockSteamAPI


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
