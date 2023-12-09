from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Game, GameScreenshot


def get_all_games(session: Session) -> Sequence[Game]:
    return session.scalars(select(Game)).all()


def get_games_in_steam_ids(session: Session, steam_ids: Iterable[int]) -> Sequence[Game]:
    return session.scalars(select(Game).where(Game.steam_id.in_(steam_ids))).all()


def get_game_screenshots_in_steam_file_ids(
    session: Session, steam_file_ids: Iterable[int]
) -> Sequence[GameScreenshot]:
    return session.scalars(select(GameScreenshot).where(GameScreenshot.steam_file_id.in_(steam_file_ids))).all()
