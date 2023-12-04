from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Game


def get_all_games(session: Session) -> Sequence[Game]:
    return session.scalars(select(Game)).all()

