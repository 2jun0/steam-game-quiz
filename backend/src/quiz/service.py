from collections.abc import Iterable, Sequence
from datetime import datetime

from pydantic_core import Url

from ..config import settings
from . import schema
from .exception import QuizAlreadyCompletedError, QuizNotCompletedError, QuizNotFoundError
from .model import DailyQuiz, QuizAnswer
from .repository import DailyQuizRepository, QuizAnswerRepository, QuizRepository


class QuizService:
    def __init__(
        self,
        *,
        quiz_repository: QuizRepository,
        quiz_answer_repository: QuizAnswerRepository,
        daily_quiz_repository: DailyQuizRepository
    ) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository
        self._daily_quiz_repo = daily_quiz_repository

    def _today_quizzes(self, daily_quizzes: Iterable[DailyQuiz]) -> list[schema.DailyQuiz]:
        today_quizzes: list[schema.DailyQuiz] = []
        for daily_quiz in daily_quizzes:
            assert daily_quiz.quiz.id is not None

            screenshots = [Url(s.url) for s in daily_quiz.quiz.screenshots]
            today_quizzes.append(schema.DailyQuiz(quiz_id=daily_quiz.quiz_id, screenshots=screenshots))

        return today_quizzes

    async def get_today_quizzes(self) -> Sequence[schema.DailyQuiz]:
        utc_now_date = datetime.utcnow().date()

        daily_quizzes = await self._daily_quiz_repo.get_by_target_date_with_quiz(target_date=utc_now_date)
        return self._today_quizzes(daily_quizzes)

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
