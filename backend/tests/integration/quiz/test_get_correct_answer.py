from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.auth.model import User
from src.config import settings
from tests.utils.quiz import create_random_quiz, create_random_quiz_answer


def test_get_correct_answer_with_correct_submission(client: TestClient, session: Session, current_user: User):
    quiz = create_random_quiz(session)
    create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=True)

    res = client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": quiz.game.name}


def test_get_correct_answer_with_exceed_submission_limit(client: TestClient, session: Session, current_user: User):
    quiz = create_random_quiz(session)
    [
        create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=False)
        for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT)
    ]

    res = client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": quiz.game.name}


def test_get_correct_answer_with_unauthorized_request(client: TestClient):
    quiz_id = 1

    res = client.get(f"/quiz/correct_answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_correct_answer_with_not_existed_quiz_id(client: TestClient, current_user: User):
    quiz_id = 1

    res = client.get(f"/quiz/correct_answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_correct_answer_with_not_completed_quiz(client: TestClient, session: Session, current_user: User):
    quiz = create_random_quiz(session)

    res = client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
