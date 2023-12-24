from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from .dependency import get_quiz_service
from .service import QuizService

router = APIRouter()


@cbv(router)
class QuizCBV:
    service: QuizService = Depends(get_quiz_service)

    @router.get("/quiz/daily_quizes")
    def get_daily_quizes(self):
        return self.service.get_today_quizes()
