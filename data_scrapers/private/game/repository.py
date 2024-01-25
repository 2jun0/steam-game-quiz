from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Game


def get_all_games(session: Session) -> Sequence[Game]:
    return session.scalars(select(Game)).all()


def get_games_in_steam_ids(session: Session, steam_ids: Sequence[int]) -> Sequence[Game]:
    return session.scalars(select(Game).where(Game.steam_id.in_(steam_ids))).all()
