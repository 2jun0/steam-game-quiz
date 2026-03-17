from datetime import datetime

from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from tests.utils.quiz import create_random_daily_quiz


async def test_get_daily_quizzes(client: AsyncClient, session: AsyncSession):
    today = datetime.utcnow().date()
    saved_daily_quizzes = [await create_random_daily_quiz(session, target_date=today) for _ in range(5)]

    res = await client.get("/quiz/daily_quizes")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["daily_quizes"]) == 5
    for daily_quiz_json, saved_daily_quiz in zip(res_json["daily_quizes"], saved_daily_quizzes):
        assert len(daily_quiz_json["screenshots"]) == 5
        assert daily_quiz_json["screenshots"] == [
            s.url for s in (await (await saved_daily_quiz.awt_quiz).awt_screenshots)
        ]
        assert daily_quiz_json["quiz_id"] == saved_daily_quiz.quiz_id
        assert daily_quiz_json["feature"] == saved_daily_quiz.feature
