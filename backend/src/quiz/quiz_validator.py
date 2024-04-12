from collections.abc import Sequence
from typing import Optional

from .exception import QuizAlreadyCompletedError, QuizNotCompletedError, QuizNotFoundError
from .model import Quiz
from .quiz_manager import IQuizAnswer, QuizManager


class QuizValidator:

    def __init__(self, *, quiz_manager: QuizManager) -> None:
        self._quiz_manager = quiz_manager

    def validate_quiz_not_completed(self, *, answers: Sequence[IQuizAnswer]):
        if self._quiz_manager.is_quiz_completed(answers=answers):
            raise QuizAlreadyCompletedError

    def validate_quiz_completed(self, *, answers: Sequence[IQuizAnswer]):
        if not self._quiz_manager.is_quiz_completed(answers=answers):
            raise QuizNotCompletedError

    def validate_quiz_existed(self, *, quiz: Optional[Quiz]) -> Quiz:
        if quiz is None:
            raise QuizNotFoundError

        return quiz
