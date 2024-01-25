from typing import Optional, Sequence

from ..logger import logger
from ..protocols import LambdaAPI, SteamAPI
from ..steam.exception import SteamAPINoContentsException
from .model import NewGame


def _put_kor_name_in_new_game(steam_api: SteamAPI, game: NewGame) -> None:
    try:
        game_detail = steam_api.get_game_details(game.steam_id, language="korean")
        game.kr_name = game_detail.name
    except SteamAPINoContentsException:
        pass  # game.kr_name will none


def _put_game_detail_in_new_game(steam_api: SteamAPI, game: NewGame) -> None:
    game_detail = steam_api.get_game_details_from_gamalytic(game.steam_id)

    game.genres = game_detail.genres
    game.released_at = game_detail.released_at


def _remove_existed_new_games(lambda_api: LambdaAPI, games: Sequence[NewGame]) -> list[NewGame]:
    steam_id2game = {g.steam_id: g for g in games}
    exists = set(g.steam_id for g in lambda_api.get_games_in_steam_ids(list(steam_id2game.keys())))

    return [steam_id2game[steam_id] for steam_id in steam_id2game.keys() - exists]


def _update_game_details(steam_api: SteamAPI, game: NewGame) -> Optional[NewGame]:
    try:
        # put game detail
        _put_game_detail_in_new_game(steam_api, game)

        # update korean game name
        _put_kor_name_in_new_game(steam_api, game)
        return game
    except SteamAPINoContentsException as e:
        logger.info(e)
        return None


def scrap_games(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    games: list[NewGame] = []

    # get feature games
    logger.info("getting feature games")
    for g in steam_api.get_feature_games():
        games.append(NewGame(steam_id=g.app_id, name=g.name))
    logger.info("feature games: %s", games)

    # remove existed games
    logger.info("removing existed games")
    new_games = _remove_existed_new_games(lambda_api, games)
    logger.info("remain games: %s", new_games)

    # update game details
    logger.info("update game details")
    updated_new_games: list[NewGame] = []
    for new_game in new_games:
        game = _update_game_details(steam_api, new_game)
        if game is None:
            continue

        updated_new_games.append(game)
    logger.info("updated games: %s", updated_new_games)

    # filter unfamous game
    logger.info("filtering owner count < 100,000")
    filtered_games: list[NewGame] = []
    for new_game in updated_new_games:
        if new_game.owners < 100_000:  # type: ignore
            continue

        filtered_games.append(new_game)
    logger.info("filtered games: %s", filtered_games)

    # save new games
    lambda_api.save_games(filtered_games)
    logger.info("saved games: %s", filtered_games)
