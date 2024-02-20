from typing import Annotated

from fastapi import Depends

from ..dependency import ElasticSearchClientDep
from .service import GameService


async def get_game_service(es_client: ElasticSearchClientDep) -> GameService:
    return GameService(es_client)


GameServiceDep = Annotated[GameService, Depends(get_game_service)]
