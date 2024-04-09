from typing import Annotated

from fastapi import Depends

from ..dependency import ElasticSearchClientDep, SessionDep
from .repository import SolvedGameRepository
from .service import GameService


async def get_solved_game_repository(session: SessionDep):
    return SolvedGameRepository(session)


async def get_game_service(
    es_client: ElasticSearchClientDep, solved_game_repository: "SolvedGameRepositoryDep"
) -> GameService:
    return GameService(es_client=es_client, solved_game_repository=solved_game_repository)


GameServiceDep = Annotated[GameService, Depends(get_game_service)]
SolvedGameRepositoryDep = Annotated[SolvedGameRepository, Depends(get_solved_game_repository)]
