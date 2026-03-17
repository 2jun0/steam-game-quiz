from fastapi import status
from httpx import AsyncClient

from src.auth.model import User


async def test_get_me(client: AsyncClient, current_user: User):
    current_user.rank_score = 100

    res = await client.get("/me")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json["email"] == current_user.email
    assert res_json["rank_score"] == current_user.rank_score
