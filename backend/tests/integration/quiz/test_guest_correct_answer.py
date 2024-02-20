import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.config import settings
from tests.utils.quiz import create_random_quiz


def test_get_guest_correct_answer_with_correct_submission(client: TestClient, session: Session):
    quiz = create_random_quiz(session)

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            quiz.id: [{"answer": quiz.game.name, "correct": True, "created_at": "2024-02-20T16:02:01.816Z"}]
        },
    }

    res = client.get(f"/quiz/guest/correct_answer?quiz_id={quiz.id}", cookies={"guest": json.dumps(guest)})
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": quiz.game.name}


def test_get_guest_correct_answer_with_exceed_submission_limit(client: TestClient, session: Session):
    quiz = create_random_quiz(session)
    wrong_answer = quiz.game.name + "haha"

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            quiz.id: [
                {"answer": wrong_answer, "correct": False, "created_at": "2024-02-20T16:02:01.816Z"}
                for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT)
            ]
        },
    }

    res = client.get(f"/quiz/guest/correct_answer?quiz_id={quiz.id}", cookies={"guest": json.dumps(guest)})
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": quiz.game.name}


def test_get_guest_correct_answer_with_not_existed_quiz_id(client: TestClient):
    quiz_id = 1

    res = client.get(f"/quiz/guest/correct_answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_guest_correct_answer_with_not_completed_quiz(client: TestClient, session: Session):
    quiz = create_random_quiz(session)

    res = client.get(f"/quiz/guest/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
