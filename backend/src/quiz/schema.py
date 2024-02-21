from datetime import datetime
from typing import Sequence

from pydantic import BaseModel, HttpUrl


class DailyQuiz(BaseModel):
    quiz_id: int
    screenshots: Sequence[HttpUrl]
    feature: str


class DailyQuizzesResponse(BaseModel):
    daily_quizes: Sequence[DailyQuiz]


class SubmitAnswerRequest(BaseModel):
    quiz_id: int
    answer: str


class SubmitAnswerResponse(BaseModel):
    correct: bool


class QuizAnswer(BaseModel):
    answer: str
    correct: bool
    created_at: datetime


class QuizAnswerResponse(BaseModel):
    quiz_answers: Sequence[QuizAnswer]


class CorrectAnswerResponse(BaseModel):
    correct_answer: str
