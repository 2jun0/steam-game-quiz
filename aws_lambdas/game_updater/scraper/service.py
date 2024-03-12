from .alias import scrap_aliases
from ..protocols import LambdaAPI, SteamAPI
from . import game as game_scraper
from ..logger import logger
from ..aws_lambda.model import SaveGame


def update_games(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    games = game_scraper.scrap_games(steam_api)
    aliases = scrap_aliases([game.steam_id for game in games])

    # save games
    logger.info("saving games")
    lambda_api.save_games(
        [
            SaveGame(
                steam_id=g.steam_id,
                name=g.name,
                released_at=g.released_at,
                genres=g.genres,
                aliases=aliases[g.steam_id],
            )
            for g in games
        ]
    )
