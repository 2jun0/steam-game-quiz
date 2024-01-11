from typing import Annotated

from fastapi import Depends

from ..dependency import SessionDep
from .repository import QuizRepository, QuizSubmitRepository
from .service import QuizService


async def get_quiz_service(
    quiz_repository: "QuizRepositoryDep", quiz_submit_repository: "QuizSubmitRepositoryDep"
) -> QuizService:
    return QuizService(quiz_repository=quiz_repository, quiz_submit_repository=quiz_submit_repository)


async def get_quiz_repository(session: SessionDep) -> QuizRepository:
    return QuizRepository(session)


async def get_quiz_submit_repository(session: SessionDep) -> QuizSubmitRepository:
    return QuizSubmitRepository(session)


QuizRepositoryDep = Annotated[QuizRepository, Depends(get_quiz_repository)]
QuizSubmitRepositoryDep = Annotated[QuizSubmitRepository, Depends(get_quiz_submit_repository)]
QuizServiceDep = Annotated[QuizService, Depends(get_quiz_service)]
