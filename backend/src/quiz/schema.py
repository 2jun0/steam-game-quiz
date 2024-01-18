from typing import Sequence

from pydantic import BaseModel, HttpUrl


class DailyQuizesResponse(BaseModel):
    class DailyQuiz(BaseModel):
        screenshots: Sequence[HttpUrl]

    daily_quizes: Sequence[DailyQuiz]


class SubmitAnswerRequest(BaseModel):
    quiz_id: int
    answer: str


class SubmitAnswerResponse(BaseModel):
    correct: bool
