from typing import Annotated

from fastapi import Depends

from ..dependency import SessionDep
from .repository import DailyQuizRepository, QuizAnswerRepository, QuizRepository
from .service import QuizService


async def get_quiz_service(
    quiz_repository: "QuizRepositoryDep",
    quiz_submit_repository: "QuizAnswerRepositoryDep",
    daily_quiz_repository: "DailyQuizRepositoryDep",
) -> QuizService:
    return QuizService(
        quiz_repository=quiz_repository,
        quiz_answer_repository=quiz_submit_repository,
        daily_quiz_repository=daily_quiz_repository,
    )


async def get_quiz_repository(session: SessionDep) -> QuizRepository:
    return QuizRepository(session)


async def get_quiz_answer_repository(session: SessionDep) -> QuizAnswerRepository:
    return QuizAnswerRepository(session)


async def get_daily_quiz_repository(session: SessionDep) -> DailyQuizRepository:
    return DailyQuizRepository(session)


QuizRepositoryDep = Annotated[QuizRepository, Depends(get_quiz_repository)]
QuizAnswerRepositoryDep = Annotated[QuizAnswerRepository, Depends(get_quiz_answer_repository)]
DailyQuizRepositoryDep = Annotated[DailyQuizRepository, Depends(get_daily_quiz_repository)]
QuizServiceDep = Annotated[QuizService, Depends(get_quiz_service)]
