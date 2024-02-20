import base64
import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.quiz import create_random_quiz
from tests.utils.utils import jsontime2datetime


def test_get_guest_answer(session: Session, client: TestClient):
    quiz = create_random_quiz(session)
    wrong_answers = ["빙빙바리바리구1", "빙빙바리바리구2", "빙빙바리바리구3"]

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            str(quiz.id): [
                {"answer": answer, "correct": False, "created_at": "2024-02-20T16:02:01.816Z"}
                for answer in wrong_answers
            ]
        },
    }

    res = client.get(
        f"/quiz/guest/answer?quiz_id={quiz.id}",
        cookies={"guest": base64.b64encode(json.dumps(guest).encode()).decode()},
    )
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    # 제출(저장) 순서도 동일해야 한다.
    for quiz_ans_res, quiz_ans in zip(res_json["quiz_answers"], guest["quiz_answers"][str(quiz.id)]):
        assert quiz_ans_res["answer"] == quiz_ans["answer"]
        assert quiz_ans_res["correct"] == quiz_ans["correct"]
        assert jsontime2datetime(quiz_ans_res["created_at"]) == jsontime2datetime(quiz_ans["created_at"])


def test_get_guest_answer_with_not_existed_quiz_id(client: TestClient):
    quiz_id = 1

    res = client.get(f"/quiz/guest/answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
