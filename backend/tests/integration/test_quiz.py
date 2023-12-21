import pytest
from async_asgi_testclient import TestClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_daily_quizes(client: TestClient):
    res = await client.get("/quiz/daily_quizes")
    assert res.status_code == status.HTTP_200_OK

    # TODO: 데일리 퀴즈 5개인지 검증, 퀴즈에 1개의 스크린샷이 있는지 확인
    # res_json = res.json()
