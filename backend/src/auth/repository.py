from sqlmodel.ext.asyncio.session import AsyncSession

from ..repository import CRUDMixin, IRepository
from .model import User


class UserRepository(IRepository[User], CRUDMixin):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
