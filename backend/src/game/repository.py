from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..repository import CRUDMixin, IRepository
from .model import SolvedGame


class SolvedGameRepository(IRepository[SolvedGame], CRUDMixin):
    model = SolvedGame

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_and_game(self, *, user_id: int, game_id: int) -> SolvedGame:
        stmt = select(SolvedGame).where(SolvedGame.user_id == user_id, SolvedGame.game_id == game_id)
        rs = await self._session.exec(stmt)
        return rs.one()

    async def exists_by_user_and_game(self, *, user_id: int, game_id: int) -> bool:
        stmt = select(SolvedGame).where(SolvedGame.user_id == user_id, SolvedGame.game_id == game_id)
        rs = await self._session.exec(stmt)
        return rs.one_or_none() is not None
