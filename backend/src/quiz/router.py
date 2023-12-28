from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from .dependency import get_quiz_service
from .schema import DailyQuizesResponse
from .service import QuizService

router = APIRouter()


@cbv(router)
class QuizCBV:
    service: QuizService = Depends(get_quiz_service)

    @router.get("/quiz/daily_quizes")
    def get_daily_quizes(self) -> DailyQuizesResponse:
        quizes = self.service.get_today_quizes()

        return DailyQuizesResponse(
            daily_quizes=[
                DailyQuizesResponse.DailyQuiz(screenshots=[s.url for s in quiz.screenshots]) for quiz in quizes
            ]
        )
