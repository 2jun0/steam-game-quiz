from collections.abc import Iterable
from typing import Any

import meilisearch

from ..es import GAME_INDEX
from ..utils import is_aldecimal
from .model import Game


def _game_docs(games: Iterable[Game]) -> list[dict[str, Any]]:
    docs = []
    for game in games:
        q_name = "".join([c if is_aldecimal(c) else " " for c in game.name])
        docs.append({
            "id": game.id,
            "name": game.name,
            "q_name": q_name,
            "aliases": [alias.name for alias in game.aliases],
        })
    return docs


def save_docs(ms_client: meilisearch.Client, *, games: Iterable[Game]):
    docs = _game_docs(games)
    task = ms_client.index(GAME_INDEX).add_documents(docs, primary_key="id")
    ms_client.wait_for_task(task.task_uid)
