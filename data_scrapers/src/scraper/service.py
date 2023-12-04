from sqlalchemy.orm import Session

from . import repository, steam_api
from .model import Game, GameScreenshot


def _put_kor_name_in_game(game: Game) -> None:
    response = steam_api.get_game_details(game.steam_id, language="korean")

    game_details = response[str(game.steam_id)]["data"]
    kr_name = game_details["name"]

    game.kr_name = kr_name


def scrap_games(session: Session) -> None:
    games = []

    # get top 100 games in 2 weeks
    response = steam_api.get_top_100_games_in_2weeks()
    for str_steam_id, detail in response.items():
        game = Game(steam_id=int(str_steam_id), name=detail["name"])
        games.append(game)

    # update korean game name
    for game in games:
        _put_kor_name_in_game(game)

    session.add_all(games)


def scrap_game_screenshot(session: Session, game: Game) -> None:
    game_screenshots = []

    response = steam_api.get_game_screenshots(game.steam_id)
    json_screenshots: list[dict[str, any]] = response["hub"]

    for json_screenshot in json_screenshots:
        steam_file_id: int = int(json_screenshot["published_file_id"])
        image_url: str = json_screenshot["full_image_url"]
        game_screenshot = GameScreenshot(
            steam_file_id=steam_file_id,
            url=image_url,
            provider="steam",
        )
        game_screenshots.append(game_screenshot)

    session.add_all(game_screenshots)


def scrap_game_screenshot_for_all(session: Session) -> None:
    games = repository.get_all_games(session)

    for game in games:
        scrap_game_screenshot(session, game)
