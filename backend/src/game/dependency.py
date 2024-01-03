from typing import Annotated

from fastapi import Depends

from ..dependency import SessionDep
from .service import GameService


def get_game_service(session: SessionDep) -> GameService:
    return GameService(session)


GameServiceDep = Annotated[GameService, Depends(get_game_service)]
