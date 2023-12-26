import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from src.quiz.model import Quiz
from tests.utils.quiz import create_random_quiz


@pytest.mark.asyncio
async def test_get_daily_quizes(client: TestClient):
    quiz: Quiz = await create_random_quiz()

    res = await client.get("/quiz/daily_quizes")
    assert res.status_code == status.HTTP_200_OK

    # TODO: 저장한 정보와 응답을 비교
    res_json = res.json()
    assert len(res_json["daily_quizes"]) == 5
    for daily_quiz_json in res_json["daily_quizes"]:
        assert len(daily_quiz_json["screenshots"]) == 5
