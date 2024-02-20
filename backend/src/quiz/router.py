from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from ..auth.dependency import CURRENT_USER_DEP
from .daily_quiz_loader import DailyQuizLoader
from .dependency import get_daily_quiz_loader, get_quiz_service
from .schema import (
    CorrectAnswerResponse,
    DailyQuizzesResponse,
    QuizAnswer,
    QuizAnswerResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from .service import QuizService

router = APIRouter()


@cbv(router)
class QuizCBV:
    service: QuizService = Depends(get_quiz_service)
    daily_quiz_loader: DailyQuizLoader = Depends(get_daily_quiz_loader)

    @router.get("/quiz/daily_quizes")
    async def get_daily_quizzes(self) -> DailyQuizzesResponse:
        quizzes = await self.daily_quiz_loader.get_daily_quizzes()
        return DailyQuizzesResponse(daily_quizes=quizzes)

    @router.post("/quiz/submit_answer")
    async def submit_answer(
        self, quiz_submit_req: SubmitAnswerRequest, current_user: CURRENT_USER_DEP
    ) -> SubmitAnswerResponse:
        correct = await self.service.submit_answer(
            quiz_id=quiz_submit_req.quiz_id, user_id=current_user.id, answer=quiz_submit_req.answer
        )
        return SubmitAnswerResponse(correct=correct)

    @router.get("/quiz/answer")
    async def get_quiz_answer(self, quiz_id: int, current_user: CURRENT_USER_DEP) -> QuizAnswerResponse:
        quiz_answers = await self.service.get_quiz_answer(quiz_id=quiz_id, user_id=current_user.id)

        return QuizAnswerResponse(
            quiz_answers=[
                QuizAnswer(answer=qa.answer, correct=qa.correct, created_at=qa.created_at) for qa in quiz_answers
            ]
        )

    @router.get("/quiz/correct_answer")
    async def get_correct_answer(self, quiz_id: int, current_user: CURRENT_USER_DEP):
        correct_answer = await self.service.get_correct_answer(quiz_id=quiz_id, user_id=current_user.id)

        return CorrectAnswerResponse(correct_answer=correct_answer)
