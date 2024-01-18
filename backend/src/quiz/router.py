from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from pydantic_core import Url

from ..auth.dependency import CURRENT_USER_DEP
from .dependency import get_quiz_service
from .schema import DailyQuizesResponse, QuizSubmitRequest, QuizSubmitResponse
from .service import QuizService

router = APIRouter()


@cbv(router)
class QuizCBV:
    service: QuizService = Depends(get_quiz_service)

    @router.get("/quiz/daily_quizes")
    async def get_daily_quizes(self) -> DailyQuizesResponse:
        quizes = await self.service.get_today_quizes()

        return DailyQuizesResponse(
            daily_quizes=[
                DailyQuizesResponse.DailyQuiz(screenshots=[Url(s.url) for s in quiz.screenshots]) for quiz in quizes
            ]
        )

    @router.post("/quiz/submit_answer")
    async def submit_answer(
        self, quiz_submit_req: QuizSubmitRequest, current_user: CURRENT_USER_DEP
    ) -> QuizSubmitResponse:
        correct = await self.service.submit_answer(
            quiz_id=quiz_submit_req.quiz_id, user_id=current_user.id, answer=quiz_submit_req.answer
        )
        return QuizSubmitResponse(correct=correct)
