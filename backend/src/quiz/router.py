from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from .dependency import get_quiz_service
from .service import QuizService

router = InferringRouter()


@cbv(router)
class QuizCBV:
    service: QuizService = Depends(get_quiz_service)

    @router.get("/quiz/daliy_quizes")
    def get_daliy_quizes(self):
        return self.service.get_today_quizes()
