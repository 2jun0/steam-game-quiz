from datetime import datetime, time
from typing import Sequence

from pydantic_core import Url

from ..config import settings
from .exception import QuizAlreadyCompletedError, QuizNotCompletedError, QuizNotFoundError
from .model import Quiz, QuizAnswer
from .repository import QuizAnswerRepository, QuizRepository
from .schema import DailyQuiz


class QuizService:
    def __init__(self, *, quiz_repository: QuizRepository, quiz_answer_repository: QuizAnswerRepository) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository

    def _today_quizzes(self, quizzes: Sequence[Quiz]) -> list[DailyQuiz]:
        daily_quizzes: list[DailyQuiz] = []
        for quiz in quizzes:
            assert quiz.id is not None

            screenshots = [Url(s.url) for s in quiz.screenshots]
            daily_quizzes.append(DailyQuiz(quiz_id=quiz.id, screenshots=screenshots))

        return daily_quizzes

    async def get_today_quizzes(self) -> Sequence[DailyQuiz]:
        now = datetime.utcnow()
        today = now.date()
        start_at = datetime.combine(today, time.min)
        end_at = datetime.combine(today, time.max)

        quizzes = await self._quiz_repo.get_by_created_at_interval_with_screenshots(start_at=start_at, end_at=end_at)
        return self._today_quizzes(quizzes)

    async def submit_answer(self, *, quiz_id: int, user_id: int, answer: str) -> bool:
        """퀴즈에 대한 정답 여부를 반환하는 함수"""
        quiz = await self._quiz_repo.get_with_game(id=quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        quiz_answers = await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)
        if self._is_quiz_completed(answers=quiz_answers):
            raise QuizAlreadyCompletedError

        correct = quiz.game.name == answer
        quiz_submit = QuizAnswer(answer=answer, correct=correct, quiz_id=quiz_id, user_id=user_id)

        await self._quiz_answer_repo.create(model=quiz_submit)

        return correct

    async def get_quiz_answer(self, *, quiz_id: int, user_id: int) -> Sequence[QuizAnswer]:
        quiz = await self._quiz_repo.get(id=quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        return await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)

    async def get_correct_answer(self, *, quiz_id: int, user_id: int) -> str:
        quiz = await self._quiz_repo.get_with_game(id=quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        quiz_answers = await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)
        if not self._is_quiz_completed(answers=quiz_answers):
            raise QuizNotCompletedError

        return quiz.game.name

    def _is_quiz_completed(self, *, answers: Sequence[QuizAnswer]) -> bool:
        return self._has_correct_answer(answers=answers) or self._is_submission_limit_reached(answers=answers)

    def _has_correct_answer(self, *, answers: Sequence[QuizAnswer]) -> bool:
        for answer in answers:
            if answer.correct:
                return True

        return False

    def _is_submission_limit_reached(self, *, answers: Sequence[QuizAnswer]) -> bool:
        return len(answers) >= settings.QUIZ_ANSWER_SUBMISSION_LIMIT
