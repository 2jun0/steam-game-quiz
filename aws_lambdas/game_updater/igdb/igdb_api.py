from collections.abc import Callable, Iterable, Sequence
from functools import cache, wraps
from typing import Any
from ..config import setting

import requests

STEAM_CATEGORY = 1
MAX_LIMIT = 500


def batch(size: int):
    def batch_decorator(func: Callable[[Sequence[int]], list]):

        @wraps(func)
        def wrapper(_input: Sequence[int], **kwargs):
            outputs = []

            for srt_idx in range(0, len(_input), size):
                batch_input = _input[srt_idx : srt_idx + size]
                batch_output = func(batch_input, **kwargs)
                outputs.extend(batch_output)

            return outputs

        return wrapper

    return batch_decorator


@cache
def _get_token():
    res = requests.post(
        "https://id.twitch.tv/oauth2/token",
        f"?client_id={setting.IGDB_CLIENT_ID}&client_secret={setting.IGDB_CLIENT_SECRET}&grant_type=client_credentials",
    )
    token = res.json()["access_token"]
    return token


def get_external_games(steam_ids: Iterable, category: int, limit: int = MAX_LIMIT) -> list[Any]:
    # category,checksum,countries,created_at,game,media,name,platform,uid,updated_at,url,year;

    uids = ",".join([f'"{id}"' for id in steam_ids])
    token = _get_token()

    response = requests.post(
        "https://api.igdb.com/v4/external_games",
        **{
            "headers": {"Client-ID": setting.IGDB_CLIENT_ID, "Authorization": f"Bearer {token}"},
            "data": f"fields game,uid; where uid=({uids}) & category={STEAM_CATEGORY}; limit {limit};",
        },
    )
    response.raise_for_status()

    return response.json()


def get_steam_games(steam_ids: Iterable, limit: int = MAX_LIMIT) -> list[Any]:
    return get_external_games(steam_ids, STEAM_CATEGORY, limit)


def get_games(ids: Iterable[int], limit: int = MAX_LIMIT) -> list[Any]:
    # checksum,cover,created_at,game,name,region,updated_at;

    ids_ = ",".join(map(str, ids))
    token = _get_token()

    response = requests.post(
        "https://api.igdb.com/v4/games",
        **{
            "headers": {"Client-ID": setting.IGDB_CLIENT_ID, "Authorization": f"Bearer {token}"},
            "data": f"fields alternative_names; where id=({ids_}); limit {limit};",
        },
    )
    response.raise_for_status()

    return response.json()


def get_alternative_names(ids: Iterable[int], limit: int = MAX_LIMIT) -> list[Any]:
    # checksum,cover,created_at,game,name,region,updated_at;

    ids_ = ",".join(map(str, ids))
    token = _get_token()

    response = requests.post(
        "https://api.igdb.com/v4/alternative_names",
        **{
            "headers": {"Client-ID": setting.IGDB_CLIENT_ID, "Authorization": f"Bearer {token}"},
            "data": f"fields name,game; where id=({ids_}); limit {limit};",
        },
    )
    response.raise_for_status()

    return response.json()


@batch(MAX_LIMIT)
def get_steam_games_batch(steam_ids: Sequence[int]) -> list[Any]:
    if len(steam_ids) == 0:
        return []

    return get_steam_games(steam_ids=steam_ids)


@batch(MAX_LIMIT)
def get_games_batch(game_ids: Sequence[int]) -> list[Any]:
    if len(game_ids) == 0:
        return []

    return get_games(ids=game_ids)


@batch(MAX_LIMIT)
def get_alternative_names_batch(alternative_name_ids: Sequence[int]) -> list[Any]:
    if len(alternative_name_ids) == 0:
        return []

    return get_alternative_names(ids=alternative_name_ids)
