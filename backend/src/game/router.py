from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from .dependency import get_game_service
from .service import GameService

router = APIRouter()


@cbv(router)
class GameCBV:
    service: GameService = Depends(get_game_service)

    @router.get("/game/auto_complete_name")
    def auto_complete_name(self, query: str):
        return 0
