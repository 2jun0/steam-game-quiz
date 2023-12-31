from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from pydantic_core import Url

from .dependency import get_quiz_service
from .schema import DailyQuizesResponse, QuizSubmitRequest
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
                DailyQuizesResponse.DailyQuiz(screenshots=[Url(s.url) for s in quiz.screenshots]) for quiz in quizes
            ]
        )

    @router.post("/quiz/submit_answer")
    def submit_answer(self, quiz_submit_req: QuizSubmitRequest) -> bool:
        return self.service.submit_answer(quiz_id=quiz_submit_req.quiz_id, answer=quiz_submit_req.answer)
