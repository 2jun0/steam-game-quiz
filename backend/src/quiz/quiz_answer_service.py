from collections.abc import Sequence

from ..game.service import GameService
from .model import Quiz, QuizAnswer
from .quiz_validator import QuizValidator
from .repository import QuizAnswerRepository, QuizRepository


class QuizAnswerService:
    def __init__(
        self,
        *,
        quiz_repository: QuizRepository,
        quiz_answer_repository: QuizAnswerRepository,
        quiz_validator: QuizValidator,
        game_service: GameService
    ) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository
        self._quiz_validator = quiz_validator
        self._game_service = game_service

    async def submit_answer(self, *, quiz_id: int, user_id: int, answer: str) -> bool:
        """퀴즈에 대한 정답 여부를 반환하는 함수"""
        quiz = await self._validate_quiz(quiz_id=quiz_id)

        correct_answer = await self._get_correct_answer(quiz=quiz)
        quiz_answers = await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)
        self._quiz_validator.validate_quiz_not_completed(answers=quiz_answers)

        correct = correct_answer == answer
        quiz_submit = QuizAnswer(answer=answer, correct=correct, quiz_id=quiz_id, user_id=user_id)
        await self._quiz_answer_repo.create(model=quiz_submit)

        if correct:
            await self._on_correct_answer(quiz=quiz, user_id=user_id)

        return correct

    async def get_quiz_answer(self, *, quiz_id: int, user_id: int) -> Sequence[QuizAnswer]:
        await self._validate_quiz(quiz_id=quiz_id)
        return await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)

    async def _on_correct_answer(self, *, quiz: Quiz, user_id: int):
        game = await quiz.get_game()
        assert game.id is not None
        await self._game_service.on_correct_answer(user_id=user_id, game_id=game.id)

    async def _validate_quiz(self, *, quiz_id: int) -> Quiz:
        quiz = await self._quiz_repo.get(id=quiz_id)
        return self._quiz_validator.validate_quiz_existed(quiz=quiz)

    async def _get_correct_answer(self, *, quiz: Quiz) -> str:
        game = await quiz.get_game()
        return game.name
