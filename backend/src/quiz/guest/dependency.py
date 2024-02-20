from ..dependency import QuizRepositoryDep, QuizValidatorDep
from .guest_quiz_service import GuestQuizService


def get_guest_quiz_service(
    quiz_repository: QuizRepositoryDep,
    quiz_validator: QuizValidatorDep,
) -> GuestQuizService:
    return GuestQuizService(quiz_repository=quiz_repository, quiz_validator=quiz_validator)
