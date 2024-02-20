from collections import defaultdict
from uuid import UUID

from pydantic import BaseModel

from ..quiz.schema import QuizAnswer

QUIZ_ID = int


class Guest(BaseModel):
    id: UUID
    quiz_answers: defaultdict[QUIZ_ID, list[QuizAnswer]] = defaultdict(list)
