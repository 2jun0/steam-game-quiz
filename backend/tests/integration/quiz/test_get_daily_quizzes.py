from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.quiz import create_random_daily_quiz


def test_get_daily_quizzes(client: TestClient, session: Session):
    today = datetime.utcnow().date()
    saved_daily_quizzes = [create_random_daily_quiz(session, target_date=today) for _ in range(5)]

    res = client.get("/quiz/daily_quizes")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["daily_quizes"]) == 5
    for daily_quiz_json, saved_daily_quiz in zip(res_json["daily_quizes"], saved_daily_quizzes):
        assert len(daily_quiz_json["screenshots"]) == 5
        assert daily_quiz_json["screenshots"] == [s.url for s in saved_daily_quiz.quiz.screenshots]
        assert daily_quiz_json["quiz_id"] == saved_daily_quiz.quiz_id
