from typing import Annotated

from fastapi import Depends

from ..dependency import ElasticSearchClientDep, SessionDep
from .manager import GameManager
from .repository import SolvedGameRepository
from .service import GameService


async def get_solved_game_repository(session: SessionDep):
    return SolvedGameRepository(session)


async def get_game_manager(solved_game_repository: "SolvedGameRepositoryDep") -> GameManager:
    return GameManager(solved_game_repository=solved_game_repository)


async def get_game_service(
    es_client: ElasticSearchClientDep, solved_game_repository: "SolvedGameRepositoryDep"
) -> GameService:
    return GameService(es_client=es_client, solved_game_repository=solved_game_repository)


SolvedGameRepositoryDep = Annotated[SolvedGameRepository, Depends(get_solved_game_repository)]
GameManagerDep = Annotated[GameManager, Depends(get_game_manager)]
GameServiceDep = Annotated[GameService, Depends(get_game_service)]
