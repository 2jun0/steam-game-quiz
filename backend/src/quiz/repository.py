from collections.abc import Sequence
from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..game.model import GameScreenshot
from ..repository import CRUDMixin, IRepository
from .model import DailyQuiz, Quiz, QuizAnswer


class QuizRepository(IRepository[Quiz], CRUDMixin):
    model = Quiz

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_with_game(self, *, id: int) -> Optional[Quiz]:
        stmt = (
            select(Quiz)
            .where(Quiz.id == id)
            .options(selectinload(Quiz.screenshots).selectinload(GameScreenshot.game))  # type: ignore
        )
        rs = await self._session.exec(stmt)
        return rs.first()

    async def get_by_created_at_interval_with_screenshots(
        self, *, start_at: datetime, end_at: datetime
    ) -> Sequence[Quiz]:
        stmts = (
            select(Quiz)
            .where(Quiz.created_at >= start_at, Quiz.created_at <= end_at)
            .options(selectinload(Quiz.screenshots))  # type: ignore
        )
        rs = await self._session.exec(stmts)
        return rs.all()


class QuizAnswerRepository(IRepository[QuizAnswer], CRUDMixin):
    model = QuizAnswer

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_quiz_id_and_user_id(self, *, quiz_id: int, user_id: int) -> Sequence[QuizAnswer]:
        stmt = select(QuizAnswer).where(QuizAnswer.quiz_id == quiz_id, QuizAnswer.user_id == user_id)
        rs = await self._session.exec(stmt)
        return rs.all()


class DailyQuizRepository(IRepository[DailyQuiz], CRUDMixin):
    model = DailyQuiz

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_target_date_with_quiz(self, *, target_date: date) -> Sequence[DailyQuiz]:
        stmt = select(DailyQuiz).where(DailyQuiz.target_date == target_date).options(selectinload(DailyQuiz.quiz))
        rs = await self._session.exec(stmt)
        return rs.all()
