import pytest
from async_asgi_testclient import TestClient
from fastapi import status
from sqlmodel import Session

from tests.utils.quiz import create_random_quiz


@pytest.mark.asyncio
async def test_post_submit_true_answer(client: TestClient, session: Session):
    saved_quiz = await create_random_quiz(session)

    res = await client.post("/quiz/submit_answer", json={"quiz_id": saved_quiz.id, "game_name": saved_quiz.game.name})
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is True


@pytest.mark.asyncio
async def test_post_submit_false_answer(client: TestClient, session: Session):
    saved_quiz = await create_random_quiz(session)

    res = await client.post("/quiz/submit_answer", json={"quiz_id": saved_quiz.id, "game_name": "빙빙바리바리구"})
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is False


@pytest.mark.asyncio
async def test_post_submit_answer_with_invalid_quiz_id(client: TestClient, session: Session):
    saved_quiz = await create_random_quiz(session)

    res = await client.post("/quiz/submit_answer", json={"quiz_id": -1, "game_name": saved_quiz.game.name})
    assert res.status_code == status.HTTP_404_NOT_FOUND
