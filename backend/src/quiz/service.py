from datetime import datetime, time
from typing import Sequence

from .exception import QuizNotFoundError
from .model import Quiz, QuizAnswer
from .repository import QuizAnswerRepository, QuizRepository


class QuizService:
    def __init__(self, *, quiz_repository: QuizRepository, quiz_answer_repository: QuizAnswerRepository) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository

    async def get_today_quizes(self) -> Sequence[Quiz]:
        now = datetime.utcnow()
        today = now.date()
        start_at = datetime.combine(today, time.min)
        end_at = datetime.combine(today, time.max)

        return await self._quiz_repo.get_by_created_at_interval_with_screenshots(start_at=start_at, end_at=end_at)

    async def submit_answer(self, *, quiz_id: int, user_id: int, answer: str) -> bool:
        """퀴즈에 대한 정답 여부를 반환하는 함수"""
        quiz = await self._quiz_repo.get_with_game(id=quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        correct = quiz.game.name == answer
        quiz_submit = QuizAnswer(answer=answer, correct=correct, quiz_id=quiz_id, user_id=user_id)

        await self._quiz_answer_repo.create(model=quiz_submit)

        return correct

    async def get_quiz_answer(self, *, quiz_id: int, user_id: int) -> Sequence[QuizAnswer]:
        quiz = await self._quiz_repo.get(id=quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        return await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)
