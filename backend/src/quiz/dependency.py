from typing import Annotated

from fastapi import Depends

from ..dependency import SessionDep
from ..game.dependency import GameServiceDep
from .daily_quiz_loader import DailyQuizLoader
from .quiz_answer_service import QuizAnswerService
from .quiz_service import QuizService
from .quiz_validator import QuizValidator
from .repository import DailyQuizRepository, QuizAnswerRepository, QuizRepository


async def get_quiz_repository(session: SessionDep) -> QuizRepository:
    return QuizRepository(session)


async def get_quiz_answer_repository(session: SessionDep) -> QuizAnswerRepository:
    return QuizAnswerRepository(session)


async def get_daily_quiz_repository(session: SessionDep) -> DailyQuizRepository:
    return DailyQuizRepository(session)


QuizRepositoryDep = Annotated[QuizRepository, Depends(get_quiz_repository)]
QuizAnswerRepositoryDep = Annotated[QuizAnswerRepository, Depends(get_quiz_answer_repository)]
DailyQuizRepositoryDep = Annotated[DailyQuizRepository, Depends(get_daily_quiz_repository)]


async def get_quiz_validator() -> QuizValidator:
    return QuizValidator()


QuizValidatorDep = Annotated[QuizValidator, Depends(get_quiz_validator)]


async def get_quiz_service(
    quiz_repository: QuizRepositoryDep,
    quiz_answer_repository: QuizAnswerRepositoryDep,
    quiz_validator: QuizValidatorDep,
) -> QuizService:
    return QuizService(
        quiz_repository=quiz_repository, quiz_answer_repository=quiz_answer_repository, quiz_validator=quiz_validator
    )


async def get_quiz_answer_service(
    quiz_repository: QuizRepositoryDep,
    quiz_answer_repository: QuizAnswerRepositoryDep,
    quiz_validator: QuizValidatorDep,
    game_service: GameServiceDep,
) -> QuizAnswerService:
    return QuizAnswerService(
        quiz_repository=quiz_repository,
        quiz_answer_repository=quiz_answer_repository,
        quiz_validator=quiz_validator,
        game_service=game_service,
    )


async def get_daily_quiz_loader(
    daily_quiz_repository: DailyQuizRepositoryDep,
):
    return DailyQuizLoader(
        daily_quiz_repository=daily_quiz_repository,
    )


QuizServiceDep = Annotated[QuizService, Depends(get_quiz_service)]
QuizAnswerServiceDep = Annotated[QuizAnswerService, Depends(get_quiz_answer_service)]
DailyQuizLoaderDep = Annotated[DailyQuizLoader, Depends(get_daily_quiz_loader)]
