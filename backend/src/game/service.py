from typing import Sequence

from sqlmodel import Session, col, select

from .model import Game


class GameService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def auto_complete_name(self, query: str) -> Sequence[str]:
        MIN_PARTIAL_QUERY_LEN = 3

        if len(query) < MIN_PARTIAL_QUERY_LEN:
            stmt = select(Game.name).where(Game.name == query)
        else:
            stmt = select(Game.name).where(col(Game.name).contains(query))

        return self._session.exec(stmt).all()
