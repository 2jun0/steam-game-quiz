from ..aws_lambda.model import Game, SaveGameScreenshot
from ..protocols import SteamAPI


def scrap_screenshots(steam_api: SteamAPI, game: Game):
    scraped = steam_api.get_game_screenshots(game.steam_id)

    return [SaveGameScreenshot(steam_file_id=s.file_id, url=s.full_image_url, game_id=game.id) for s in scraped]
