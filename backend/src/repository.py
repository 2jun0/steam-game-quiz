from typing import Generic, Protocol, Type, TypeVar

from sqlmodel import SQLModel, exists, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelTypeT = TypeVar("ModelTypeT", bound=SQLModel)
ModelTypeS = TypeVar("ModelTypeS", bound=SQLModel)


class IRepository(Protocol, Generic[ModelTypeT]):
    _session: AsyncSession
    model: Type[ModelTypeT]


class CRUDMixin:
    async def get(self: IRepository[ModelTypeS], *, id: int) -> ModelTypeS | None:
        stmt = select(self.model).where(self.model.id == id)
        rs = await self._session.exec(stmt)
        return rs.first()

    async def exists(self: IRepository[ModelTypeS], *, id: int) -> bool:
        stmt = select(exists().where(self.model.id == id))
        rs = await self._session.exec(stmt)
        return rs.one()

    async def create(self: IRepository[ModelTypeS], *, model: ModelTypeS) -> ModelTypeS:
        self._session.add(model)
        return model
