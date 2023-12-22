from datetime import datetime, time

from sqlmodel import Session, select

from .model import Quiz


class QuizService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_today_quizes(self) -> Quiz | None:
        # TODO: not a quiz but return list of quizes
        now = datetime.utcnow()
        today = now.date()
        start_datetime = datetime.combine(today, time.min)
        end_datetime = datetime.combine(today, time.max)

        stmts = select(Quiz).where(Quiz.created_at >= start_datetime, Quiz.created_at <= end_datetime)
        return self._session.exec(stmts).first()
