import pytest

from src.scraper.steam_api import get_game_details, get_game_screenshots, get_top_100_games_in_2weeks


@pytest.fixture
def app_id() -> int:
    return 70  # half-life


def test_get_top_100_geams_in_2weeks():
    assert get_top_100_games_in_2weeks()


def test_get_game_screenshots(app_id: int):
    assert get_game_screenshots(app_id)


def test_get_game_details(app_id: int):
    assert get_game_details(app_id)


def test_get_game_details_kor(app_id: int):
    assert get_game_details(app_id, "korean")
