from typing import Iterable

from sqlalchemy.orm import Session

from . import repository
from .model import Game, GameScreenshot
from .protocols import SteamAPI


def _put_kor_name_in_game(steam_api: SteamAPI, game: Game) -> None:
    game_detail = steam_api.get_game_details(game.steam_id, language="korean")
    game.kr_name = game_detail.name


def _remove_existed_games(session: Session, games: Iterable[Game]) -> set[Game]:
    steam_id2game = {g.steam_id: g for g in games}
    exists = set(g.steam_id for g in repository.get_games_in_steam_ids(session, steam_id2game.keys()))

    return set(steam_id2game[steam_id] for steam_id in steam_id2game.keys() - exists)


def _remove_existed_screenshot(session: Session, screenshots: Iterable[GameScreenshot]) -> set[GameScreenshot]:
    file_id2screenshot = {s.steam_file_id: s for s in screenshots}
    exists = set(
        s.steam_file_id for s in repository.get_game_screenshots_in_steam_file_ids(session, file_id2screenshot.keys())
    )

    return set(file_id2screenshot[file_id] for file_id in file_id2screenshot.keys() - exists)


def scrap_games(steam_api: SteamAPI, session: Session) -> None:
    games: list[Game] = []

    # get top 100 games in 2 weeks
    for g in steam_api.get_top_100_games_in_2weeks():
        games.append(Game(steam_id=g.app_id, name=g.name))

    # remove existed games
    new_games = _remove_existed_games(session, games)

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
    new_screenshots = _remove_existed_screenshot(session, screenshots)

    session.add_all(new_screenshots)


def scrap_game_screenshot_for_all(steam_api: SteamAPI, session: Session) -> None:
    games = repository.get_all_games(session)

    for game in games:
        scrap_game_screenshot(steam_api, session, game)
