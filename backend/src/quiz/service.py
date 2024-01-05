from datetime import datetime, time
from typing import Optional, Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .exception import QuizNotFoundError
from .model import Quiz


class QuizService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_today_quizes(self) -> Sequence[Quiz]:
        now = datetime.utcnow()
        today = now.date()
        start_datetime = datetime.combine(today, time.min)
        end_datetime = datetime.combine(today, time.max)

        stmts = select(Quiz).where(Quiz.created_at >= start_datetime, Quiz.created_at <= end_datetime)
        rs = await self._session.exec(stmts)
        return rs.all()

    async def submit_answer(self, *, quiz_id: int, answer: str) -> bool:
        """
        퀴즈에 대한 정답 여부를 반환하는 함수
        """

        # TODO: 제출 기록을 저장해야 함
        quiz = await self._get_quiz_by_id(quiz_id)

        if quiz is None:
            raise QuizNotFoundError

        return quiz.game.name == answer

    async def _get_quiz_by_id(self, id: int) -> Optional[Quiz]:
        stmt = select(Quiz).where(Quiz.id == id)
        rs = await self._session.exec(stmt)
        return rs.first()
