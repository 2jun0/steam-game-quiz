import base64

from fastapi import APIRouter, Depends, Response
from fastapi_restful.cbv import cbv

from ...guest.dependency import CURRENT_GUEST_DEP
from ..schema import CorrectAnswerResponse, QuizAnswerResponse, SubmitAnswerRequest, SubmitAnswerResponse
from .dependency import get_guest_quiz_service
from .guest_quiz_service import GuestQuizService

router = APIRouter()


@cbv(router)
class QuizForGuestCBV:
    service: GuestQuizService = Depends(get_guest_quiz_service)

    @router.post("/quiz/guest/submit_answer")
    async def submit_answer(
        self, quiz_submit_req: SubmitAnswerRequest, current_guest: CURRENT_GUEST_DEP, response: Response
    ) -> SubmitAnswerResponse:

        correct, new_guest = await self.service.submit_answer(
            guest=current_guest, quiz_id=quiz_submit_req.quiz_id, answer=quiz_submit_req.answer
        )

        response.set_cookie("guest", base64.b64encode(new_guest.model_dump_json().encode()).decode())
        return SubmitAnswerResponse(correct=correct)

    @router.get("/quiz/guest/answer")
    async def get_quiz_answers(self, quiz_id: int, current_guest: CURRENT_GUEST_DEP) -> QuizAnswerResponse:
        answers = await self.service.get_quiz_answer(guest=current_guest, quiz_id=quiz_id)
        return QuizAnswerResponse(quiz_answers=answers)

    @router.get("/quiz/guest/correct_answer")
    async def get_correct_answer(self, quiz_id: int, current_guest: CURRENT_GUEST_DEP):
        correct_answer = await self.service.get_correct_answer(guest=current_guest, quiz_id=quiz_id)
        return CorrectAnswerResponse(correct_answer=correct_answer)
