import pytest

from game_updater.config import setting
from game_updater.scraper.game import scrap_games
from tests.game_updater.utils.mock_steam_api import MockSteamAPI
from tests.game_updater.utils.steam import create_random_game


@pytest.fixture
def mock_steam_api() -> MockSteamAPI:
    return MockSteamAPI()


def test_scrap_games는_게임을_구한다(mock_steam_api: MockSteamAPI):
    mock_steam_api.prepare_mock_data()

    scraped = scrap_games(mock_steam_api)
    assert len(scraped) > 0


def test_scrap_games는_수익이_높은_게임만_구한다(mock_steam_api: MockSteamAPI):
    popular_game = create_random_game(revenue=setting.MIN_REVENUE, tags=[])
    unpopular_game = create_random_game(revenue=setting.MIN_REVENUE - 1, tags=[])
    mock_steam_api.add_mock_game(popular_game)
    mock_steam_api.add_mock_game(unpopular_game)

    scraped = scrap_games(mock_steam_api)

    assert len(scraped) == 1
    assert scraped[0].steam_id == popular_game["steam_id"]


@pytest.mark.parametrize("sex_tag", ("Sexual Content", "NSFW"))
def test_scrap_games는_성적인_게임을_구하지_않는다(mock_steam_api: MockSteamAPI, sex_tag: str):
    sexual_game = create_random_game(revenue=setting.MIN_REVENUE, tags=[sex_tag])
    mock_steam_api.add_mock_game(sexual_game)

    scraped = scrap_games(mock_steam_api)

    assert len(scraped) == 0
