from collections.abc import Iterable, Sequence
from datetime import datetime

from pydantic_core import Url

from . import schema
from .model import DailyQuiz
from .repository import DailyQuizRepository


class DailyQuizLoader:
    def __init__(self, *, daily_quiz_repository: DailyQuizRepository) -> None:
        self._daily_quiz_repo = daily_quiz_repository

    def _daily_quizzes(self, daily_quizzes: Iterable[DailyQuiz]) -> list[schema.DailyQuiz]:
        quizzes: list[schema.DailyQuiz] = []
        for daily_quiz in daily_quizzes:
            assert daily_quiz.quiz.id is not None

            screenshots = [Url(s.url) for s in daily_quiz.quiz.screenshots]
            quizzes.append(
                schema.DailyQuiz(quiz_id=daily_quiz.quiz_id, screenshots=screenshots, feature=daily_quiz.feature)
            )

        return quizzes

    async def get_daily_quizzes(self) -> Sequence[schema.DailyQuiz]:
        utc_now_date = datetime.utcnow().date()

        daily_quizzes = await self._daily_quiz_repo.get_by_target_date_with_quiz_and_screenshots(
            target_date=utc_now_date
        )
        return self._daily_quizzes(daily_quizzes)
