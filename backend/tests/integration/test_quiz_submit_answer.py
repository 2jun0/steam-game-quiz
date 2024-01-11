from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.quiz import create_random_quiz, get_quiz_submit


def test_post_submit_true_answer(client: TestClient, session: Session):
    saved_quiz = create_random_quiz(session)

    res = client.post("/quiz/submit_answer", json={"quiz_id": saved_quiz.id, "answer": saved_quiz.game.name})
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is True

    # check db
    submit = get_quiz_submit(session, quiz_id=saved_quiz.id)
    assert submit is not None
    assert submit.correct is True


def test_post_submit_false_answer(client: TestClient, session: Session):
    saved_quiz = create_random_quiz(session)

    res = client.post("/quiz/submit_answer", json={"quiz_id": saved_quiz.id, "answer": "빙빙바리바리구"})
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is False

    # check db
    submit = get_quiz_submit(session, quiz_id=saved_quiz.id)
    assert submit is not None
    assert submit.correct is False


def test_post_submit_answer_with_invalid_quiz_id(client: TestClient):
    res = client.post("/quiz/submit_answer", json={"quiz_id": -1, "answer": "아무거나 빙빙바리바리구"})
    assert res.status_code == status.HTTP_404_NOT_FOUND
