from typing import Iterable

from sqlalchemy.orm import Session

from . import repository
from .model import Game, GameScreenshot
from .protocols import SteamAPI


def _put_kor_name_in_game(steam_api: SteamAPI, game: Game) -> None:
    game_detail = steam_api.get_game_details(game.steam_id, language="korean")
    game.kr_name = game_detail.name


def _remove_existed_games(session: Session, games: set[Game]) -> Iterable[Game]:
    steam_ids = (game.steam_id for game in games)
    exists = set(repository.get_games_in_steam_ids(session, steam_ids))

    return games - exists


def _remove_existed_screenshot(session: Session, screenshots: set[GameScreenshot]) -> Iterable[GameScreenshot]:
    steam_file_ids = (screenshot.steam_file_id for screenshot in screenshots)
    exists = set(repository.get_game_screenshots_in_steam_file_ids(session, steam_file_ids))

    return screenshots - exists


def scrap_games(steam_api: SteamAPI, session: Session) -> None:
    games: list[Game] = []

    # get top 100 games in 2 weeks
    for g in steam_api.get_top_100_games_in_2weeks():
        games.append(Game(steam_id=g.app_id, name=g.name))

    # remove existed games
    new_games = _remove_existed_games(session, set(games))

    # update korean game name
    for game in new_games:
        _put_kor_name_in_game(steam_api, game)

    session.add_all(new_games)


def scrap_game_screenshot(steam_api: SteamAPI, session: Session, game: Game) -> None:
    # get some screenshots
    screenshots: list[GameScreenshot] = []

    for s in steam_api.get_game_screenshots(game.steam_id):
        screenshots.append(GameScreenshot(steam_file_id=s.file_id, url=s.full_image_url))

    # remove existed screenshot
    new_screenshots = _remove_existed_screenshot(session, set(screenshots))

    session.add_all(new_screenshots)


def scrap_game_screenshot_for_all(steam_api: SteamAPI, session: Session) -> None:
    games = repository.get_all_games(session)

    for game in games:
        scrap_game_screenshot(steam_api, session, game)
