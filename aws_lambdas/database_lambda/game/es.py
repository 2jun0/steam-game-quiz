from collections.abc import Generator, Iterable
from typing import Any

from elasticsearch import Elasticsearch, helpers

from ..es import GAME_INDEX
from .model import Game


def _bulk_game_data(games: Iterable[Game]) -> Generator[dict[str, Any], Any, None]:
    for game in games:
        q_name = "".join([c if c.isalnum() else " " for c in game.name])
        yield {
            "_index": GAME_INDEX,
            "_id": game.id,
            "id": game.id,
            "name": game.name,
            "q_name": q_name,
        }


def save_docs(es_client: Elasticsearch, *, games: Iterable[Game]):
    helpers.bulk(es_client, _bulk_game_data(games), refresh=True)
