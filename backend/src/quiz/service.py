from datetime import datetime, time
from typing import Sequence

from .exception import QuizNotFoundError
from .model import Quiz, QuizSubmit
from .repository import QuizRepository, QuizSubmitRepository


class QuizService:
    def __init__(self, *, quiz_repository: QuizRepository, quiz_submit_repository: QuizSubmitRepository) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_submit_repo = quiz_submit_repository

    async def get_today_quizes(self) -> Sequence[Quiz]:
        now = datetime.utcnow()
        today = now.date()
        start_at = datetime.combine(today, time.min)
        end_at = datetime.combine(today, time.max)

        return await self._quiz_repo.get_by_created_at_interval_with_screenshots(start_at=start_at, end_at=end_at)

    async def submit_answer(self, *, quiz_id: int, answer: str) -> bool:
        """퀴즈에 대한 정답 여부를 반환하는 함수"""
        quiz = await self._quiz_repo.get_with_game(id=quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        correct = quiz.game.name == answer
        quiz_submit = QuizSubmit(answer=answer, correct=correct, quiz_id=quiz_id)

        await self._quiz_submit_repo.create(model=quiz_submit)

        return correct
