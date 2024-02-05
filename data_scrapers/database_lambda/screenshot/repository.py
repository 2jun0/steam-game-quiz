from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import GameScreenshot


def get_game_screenshots_in_steam_file_ids(
    session: Session, steam_file_ids: Iterable[int]
) -> Sequence[GameScreenshot]:
    return session.scalars(select(GameScreenshot).where(GameScreenshot.steam_file_id.in_(steam_file_ids))).all()
