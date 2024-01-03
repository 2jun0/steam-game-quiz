from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from .dependency import get_game_service
from .schema import AutoCompleteNameResponse
from .service import GameService

router = APIRouter()


@cbv(router)
class GameCBV:
    service: GameService = Depends(get_game_service)

    @router.get("/game/auto_complete_name")
    def auto_complete_name(self, query: str) -> AutoCompleteNameResponse:
        names = self.service.auto_complete_name(query)
        return AutoCompleteNameResponse(games=names)
