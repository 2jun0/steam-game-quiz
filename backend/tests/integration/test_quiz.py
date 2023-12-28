import asyncio

import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from tests.utils.quiz import create_random_quiz


@pytest.mark.asyncio
async def test_get_daily_quizes(client: TestClient):
    saved_quizes = await asyncio.gather(*[create_random_quiz() for _ in range(5)])

    res = await client.get("/quiz/daily_quizes")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["daily_quizes"]) == 5
    for daily_quiz_json, saved_quiz in zip(res_json["daily_quizes"], saved_quizes):
        assert len(daily_quiz_json["screenshots"]) == 5
        assert daily_quiz_json["screenshots"] == [s.url for s in saved_quiz.screenshots]
