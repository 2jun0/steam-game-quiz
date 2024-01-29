from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.quiz import create_random_quiz


def test_get_daily_quizzes(client: TestClient, session: Session):
    saved_quizzes = [create_random_quiz(session) for _ in range(5)]

    res = client.get("/quiz/daily_quizes")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["daily_quizes"]) == 5
    for daily_quiz_json, saved_quiz in zip(res_json["daily_quizes"], saved_quizzes):
        assert len(daily_quiz_json["screenshots"]) == 5
        assert daily_quiz_json["screenshots"] == [s.url for s in saved_quiz.screenshots]
        assert daily_quiz_json["quiz_id"] == saved_quiz.id
