from collections.abc import Sequence
from typing import Protocol

from ..config import settings


class IQuizAnswer(Protocol):
    correct: bool


class QuizManager:
    def is_quiz_completed(self, *, answers: Sequence[IQuizAnswer]) -> bool:
        return self._has_correct_answer(answers=answers) or self._is_submission_limit_reached(answers=answers)

    def is_quiz_success(self, *, answers: Sequence[IQuizAnswer]):
        return self._has_correct_answer(answers=answers)

    def _has_correct_answer(self, *, answers: Sequence[IQuizAnswer]) -> bool:
        return any(answer.correct for answer in answers)

    def _is_submission_limit_reached(self, *, answers: Sequence[IQuizAnswer]) -> bool:
        return len(answers) >= settings.QUIZ_ANSWER_SUBMISSION_LIMIT
