from sqlmodel import col, or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .model import Game
from .schema import AutoCompleteName


class GameService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def auto_complete_name(self, query: str) -> list[AutoCompleteName]:
        MIN_PARTIAL_QUERY_LEN = 3

        if len(query) < MIN_PARTIAL_QUERY_LEN:
            stmt = select(Game.name, Game.kr_name).where(or_(Game.name == query, Game.kr_name == query))
        else:
            stmt = select(Game.name, Game.kr_name).where(
                or_(col(Game.name).contains(query), col(Game.kr_name).contains(query))
            )

        rs = await self._session.exec(stmt)
        return [AutoCompleteName(name=name, locale_name=kr_name) for name, kr_name in rs.all()]
