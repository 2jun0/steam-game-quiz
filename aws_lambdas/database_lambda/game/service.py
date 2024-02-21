from collections.abc import Iterable
from typing import Any

from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from . import es, repository
from .model_factory import to_models
from .schema import SaveGame


def get_all_games(*, session: Session, **kwargs) -> list[dict[str, Any]]:
    some_games = repository.get_all_games(session)

    return [g.to_dto().model_dump(mode="json") for g in some_games]


def save_games(games: Iterable[SaveGame], *, session: Session, es_client: Elasticsearch, **kwargs):
    models = to_models(session, games)
    session.add_all(models)
    es.save_docs(es_client, games=models)
