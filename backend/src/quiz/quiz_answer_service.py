from collections.abc import Sequence

from quiz.model import Quiz

from .model import QuizAnswer
from .quiz_validator import QuizValidator
from .repository import QuizAnswerRepository, QuizRepository


class QuizAnswerService:
    def __init__(
        self,
        *,
        quiz_repository: QuizRepository,
        quiz_answer_repository: QuizAnswerRepository,
        quiz_validator: QuizValidator,
    ) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository
        self._quiz_validator = quiz_validator

    async def submit_answer(self, *, quiz_id: int, user_id: int, answer: str) -> bool:
        """퀴즈에 대한 정답 여부를 반환하는 함수"""
        correct_answer = await self._get_correct_answer(quiz_id=quiz_id)
        quiz_answers = await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)
        self._quiz_validator.validate_quiz_not_completed(answers=quiz_answers)

        correct = correct_answer == answer
        quiz_submit = QuizAnswer(answer=answer, correct=correct, quiz_id=quiz_id, user_id=user_id)
        await self._quiz_answer_repo.create(model=quiz_submit)

        return correct

    async def get_quiz_answer(self, *, quiz_id: int, user_id: int) -> Sequence[QuizAnswer]:
        await self._validate_quiz(quiz_id=quiz_id)
        return await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)

    async def _validate_quiz(self, *, quiz_id: int) -> Quiz:
        quiz = await self._quiz_repo.get(id=quiz_id)
        return self._quiz_validator.validate_quiz_existed(quiz=quiz)

    async def _get_correct_answer(self, *, quiz_id: int) -> str:
        quiz = await self._validate_quiz(quiz_id=quiz_id)
        game = await quiz.get_game()
        return game.name
