from fastapi import Depends
from sqlmodel import Session

from ..dependency import get_session
from .service import QuizService


def get_quiz_service(session: Session = Depends(get_session)) -> QuizService:
    return QuizService(session)
