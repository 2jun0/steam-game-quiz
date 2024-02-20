from collections.abc import Sequence
from typing import Optional, Protocol

from ..config import settings
from .exception import QuizAlreadyCompletedError, QuizNotCompletedError, QuizNotFoundError
from .model import Quiz


class IQuizAnswer(Protocol):
    correct: bool


class QuizValidator:

    def validate_quiz_not_completed(self, *, answers: Sequence[IQuizAnswer]):
        if self._is_quiz_completed(answers=answers):
            raise QuizAlreadyCompletedError

    def validate_quiz_completed(self, *, answers: Sequence[IQuizAnswer]):
        if not self._is_quiz_completed(answers=answers):
            raise QuizNotCompletedError

    def validate_quiz_existed(self, *, quiz: Optional[Quiz]) -> Quiz:
        if quiz is None:
            raise QuizNotFoundError

        return quiz

    def _is_quiz_completed(self, *, answers: Sequence[IQuizAnswer]) -> bool:
        return self._has_correct_answer(answers=answers) or self._is_submission_limit_reached(answers=answers)

    def _has_correct_answer(self, *, answers: Sequence[IQuizAnswer]) -> bool:
        return any(answer.correct for answer in answers)

    def _is_submission_limit_reached(self, *, answers: Sequence[IQuizAnswer]) -> bool:
        return len(answers) >= settings.QUIZ_ANSWER_SUBMISSION_LIMIT
