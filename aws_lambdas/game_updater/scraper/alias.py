from collections import defaultdict
from collections.abc import Sequence


from ..igdb import igdb_api


def _scrap_igdb_game_ids(steam_ids: Sequence[int]) -> dict[int, int]:
    steam_games = igdb_api.get_games_batch(steam_ids)
    return {int(g["uid"]): g["game"] for g in steam_games if "game" in g}


def _scrap_alternative_name_ids(igdb_game_ids: Sequence[int]) -> list[int]:
    games = igdb_api.get_games_batch(igdb_game_ids)
    ids: list[int] = []
    for g in games:
        if "alternative_names" in g:
            ids.extend(g["alternative_names"])

    return ids


def _scrap_alternative_names(alternative_name_ids: Sequence[int]) -> dict[int, list[str]]:
    alternative_names = igdb_api.get_alternative_names_batch(alternative_name_ids)

    game2alter_names: dict[int, list[str]] = defaultdict(list)

    for a in alternative_names:
        game2alter_names[a["game"]].append(a["name"])

    return game2alter_names


def scrap_aliases(steam_ids: Sequence[int]) -> dict[int, list[str]]:
    igdb_game_ids = _scrap_igdb_game_ids(steam_ids)
    alter_name_ids = _scrap_alternative_name_ids(list(igdb_game_ids.values()))
    alter_names = _scrap_alternative_names(alter_name_ids)

    return {steam_id: alter_names[igdb_id] for steam_id, igdb_id in igdb_game_ids.items()}
