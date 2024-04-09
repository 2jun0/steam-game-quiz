import base64
import json
from uuid import uuid4

from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from tests.utils.quiz import create_random_quiz


async def test_get_guest_correct_answer_with_correct_submission(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            quiz.id: [
                {"answer": (await quiz.get_game()).name, "correct": True, "created_at": "2024-02-20T16:02:01.816Z"}
            ]
        },
    }

    res = await client.get(
        f"/quiz/guest/correct_answer?quiz_id={quiz.id}",
        cookies={"guest": base64.b64encode(json.dumps(guest).encode()).decode()},
    )
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": (await quiz.get_game()).name}


async def test_get_guest_correct_answer_with_exceed_submission_limit(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)
    wrong_answer = (await quiz.get_game()).name + "haha"

    guest = {
        "id": str(uuid4()),
        "quiz_answers": {
            quiz.id: [
                {"answer": wrong_answer, "correct": False, "created_at": "2024-02-20T16:02:01.816Z"}
                for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT)
            ]
        },
    }

    res = await client.get(
        f"/quiz/guest/correct_answer?quiz_id={quiz.id}",
        cookies={"guest": base64.b64encode(json.dumps(guest).encode()).decode()},
    )
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": (await quiz.get_game()).name}


async def test_get_guest_correct_answer_with_not_existed_quiz_id(client: AsyncClient):
    quiz_id = 1

    res = await client.get(f"/quiz/guest/correct_answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_get_guest_correct_answer_with_not_completed_quiz(client: AsyncClient, session: AsyncSession):
    quiz = await create_random_quiz(session)

    res = await client.get(f"/quiz/guest/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
