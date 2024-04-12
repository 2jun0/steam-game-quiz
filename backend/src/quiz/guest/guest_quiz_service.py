from datetime import datetime

from ...guest.schema import Guest
from ..model import Quiz
from ..quiz_validator import QuizValidator
from ..repository import QuizRepository
from ..schema import QuizAnswer


class GuestQuizService:
    def __init__(
        self,
        *,
        quiz_repository: QuizRepository,
        quiz_validator: QuizValidator,
    ) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_validator = quiz_validator

    async def submit_answer(self, *, guest: Guest, quiz_id: int, answer: str) -> tuple[bool, Guest]:
        quiz = await self._validate_quiz(quiz_id=quiz_id)
        correct_answer = await self._get_correct_answer(quiz=quiz)
        self._quiz_validator.validate_quiz_not_completed(answers=guest.quiz_answers[quiz_id])

        correct = correct_answer == answer
        guest.quiz_answers[quiz_id].append(QuizAnswer(answer=answer, correct=correct, created_at=datetime.utcnow()))

        return correct, guest

    async def get_quiz_answer(self, *, guest: Guest, quiz_id: int) -> list[QuizAnswer]:
        await self._validate_quiz(quiz_id=quiz_id)
        return guest.quiz_answers[quiz_id]

    async def get_correct_answer(self, *, guest: Guest, quiz_id: int) -> str:
        quiz = await self._validate_quiz(quiz_id=quiz_id)
        self._quiz_validator.validate_quiz_completed(answers=guest.quiz_answers[quiz_id])
        return await self._get_correct_answer(quiz=quiz)

    async def _get_correct_answer(self, *, quiz: Quiz) -> str:
        return (await quiz.get_game()).name

    async def _validate_quiz(self, *, quiz_id: int):
        quiz = await self._quiz_repo.get(id=quiz_id)
        return self._quiz_validator.validate_quiz_existed(quiz=quiz)
