from typing import Annotated

from fastapi import Depends

from ..dependency import SessionDep
from .service import QuizService


async def get_quiz_service(session: SessionDep) -> QuizService:
    return QuizService(session)


QuizServiceDep = Annotated[QuizService, Depends(get_quiz_service)]
