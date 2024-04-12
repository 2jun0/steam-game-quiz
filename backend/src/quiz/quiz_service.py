from .model import Quiz
from .quiz_validator import QuizValidator
from .repository import QuizAnswerRepository, QuizRepository


class QuizService:
    def __init__(
        self,
        *,
        quiz_repository: QuizRepository,
        quiz_answer_repository: QuizAnswerRepository,
        quiz_validator: QuizValidator,
    ) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository
        self._quiz_validator = quiz_validator

    async def get_correct_answer(self, *, quiz_id: int, user_id: int) -> str:
        quiz = await self._get_quiz(quiz_id=quiz_id)
        quiz_answers = await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)
        self._quiz_validator.validate_quiz_completed(answers=quiz_answers)

        return (await quiz.get_game()).name

    async def _get_quiz(self, *, quiz_id: int) -> Quiz:
        quiz = await self._quiz_repo.get(id=quiz_id)
        return self._quiz_validator.validate_quiz_existed(quiz=quiz)
