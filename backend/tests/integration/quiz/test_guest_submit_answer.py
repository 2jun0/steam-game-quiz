import base64
import json
from uuid import uuid4

from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from tests.utils.quiz import create_random_quiz


async def test_post_guest_submit_true_answer(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)

    res = await client.post(
        "/quiz/guest/submit_answer", json={"quiz_id": quiz.id, "answer": (await quiz.get_game()).name}
    )
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is True

    guest = json.loads(base64.b64decode(res.cookies["guest"]))

    quiz_answer = guest["quiz_answers"][str(quiz.id)][0]
    assert quiz_answer["answer"] == (await quiz.get_game()).name
    assert quiz_answer["correct"] is True


async def test_post_guest_submit_false_answer(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)
    wrong_answers = ["빙빙바리바리구1", "빙빙바리바리구2", "빙빙바리바리구3"]

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {},
    }

    for wrong_answer in wrong_answers:
        res = await client.post(
            "/quiz/guest/submit_answer",
            json={"quiz_id": quiz.id, "answer": wrong_answer},
            cookies={"guest": base64.b64encode(json.dumps(guest).encode()).decode()},
        )
        assert res.status_code == status.HTTP_200_OK

        res_json = res.json()
        assert res_json["correct"] is False

        guest = json.loads(base64.b64decode(res.cookies["guest"]))

        quiz_answer = guest["quiz_answers"][str(quiz.id)][-1]
        assert quiz_answer["answer"] == wrong_answer
        assert quiz_answer["correct"] is False


async def test_post_guest_submit_answer_with_not_existed_quiz_id(client: AsyncClient):
    res = await client.post("/quiz/guest/submit_answer", json={"quiz_id": -1, "answer": "아무거나 빙빙바리바리구"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_post_guest_submit_answer_with_exceed_submission_limit(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)
    wrong_answer = "빙빙바리바리구"

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            str(quiz.id): [
                {"answer": wrong_answer, "correct": False, "created_at": "2024-02-20T16:02:01.816Z"}
                for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT)
            ]
        },
    }

    res = await client.post(
        "/quiz/guest/submit_answer",
        json={"quiz_id": quiz.id, "answer": "아무거나 방방빙방"},
        cookies={"guest": base64.b64encode(json.dumps(guest).encode()).decode()},
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_guest_submit_answer_with_prior_correct_answer(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            str(quiz.id): [
                {"answer": (await quiz.get_game()).name, "correct": True, "created_at": "2024-02-20T16:02:01.816Z"}
            ]
        },
    }

    res = await client.post(
        "/quiz/guest/submit_answer",
        json={"quiz_id": quiz.id, "answer": "아무거나 방방빙방"},
        cookies={"guest": base64.b64encode(json.dumps(guest).encode()).decode()},
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
