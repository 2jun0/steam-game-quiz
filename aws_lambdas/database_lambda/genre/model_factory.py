from collections.abc import Iterable
from functools import cache

from sqlalchemy.orm import Session

from .model import Genre
from .repository import get_genre


def _create_model(session: Session, name: str) -> Genre:
    return Genre(name=name)


@cache
def _to_model(session: Session, name: str) -> Genre:
    model = get_genre(session, name=name)

    if model is None:
        return _create_model(session, name)

    return model


def to_models(session: Session, genres: Iterable[str]) -> list[Genre]:
    return [_to_model(session, genre) for genre in genres]
