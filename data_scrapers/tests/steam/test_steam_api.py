import pytest

from src.steam.exception import SteamAPINoContentsException
from src.steam.steam_api import SteamAPI


@pytest.fixture
def app_id() -> int:
    return 70  # half-life


@pytest.fixture
def no_detail_app_id() -> int:
    return 1599340  # Lost Ark


@pytest.fixture
def steam_api() -> SteamAPI:
    return SteamAPI()


def test_get_top_100_geams_in_2weeks(steam_api: SteamAPI):
    assert steam_api.get_top_100_games_in_2weeks()


def test_get_game_screenshots(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_screenshots(app_id)


def test_get_game_details(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_details(app_id)


def test_get_game_details_kor(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_details(app_id, "korean")


def test_get_game_details_no_content(steam_api: SteamAPI, no_detail_app_id: int):
    with pytest.raises(SteamAPINoContentsException):
        steam_api.get_game_details(no_detail_app_id)
