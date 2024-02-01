from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.auth.model import User
from tests.utils.quiz import create_random_quiz, create_random_quiz_answer


def test_get_correct_answer(client: TestClient, session: Session, current_user: User):
    quiz = create_random_quiz(session)
    create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=True)

    res = client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": quiz.game.name}
