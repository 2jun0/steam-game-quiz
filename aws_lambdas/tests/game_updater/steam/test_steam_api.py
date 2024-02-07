import pytest

from game_updater.steam.exception import SteamAPINoContentsException
from game_updater.steam.steam_api import SteamAPI


@pytest.fixture
def app_id() -> int:
    return 70  # half-life


@pytest.fixture
def no_detail_app_id() -> int:
    return 1599340  # Lost Ark


@pytest.fixture
def steam_api() -> SteamAPI:
    return SteamAPI()


def test_get_feature_games(steam_api: SteamAPI):
    assert steam_api.get_feature_games()


def test_get_game_screenshots(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_screenshots(app_id)


def test_get_game_details(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_details(app_id)


def test_get_game_details_kor(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_details(app_id, "korean")


def test_get_game_details_from_gamalytic(steam_api: SteamAPI, app_id: int):
    assert steam_api.get_game_details_from_gamalytic(app_id)


def test_get_game_details_no_content(steam_api: SteamAPI, no_detail_app_id: int):
    with pytest.raises(SteamAPINoContentsException):
        steam_api.get_game_details(no_detail_app_id)
