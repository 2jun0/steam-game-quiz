from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.model import User
from src.config import settings
from tests.utils.quiz import create_random_quiz, create_random_quiz_answer


async def test_get_correct_answer_with_correct_submission(
    client: AsyncClient, session: AsyncSession, current_user: User
):
    quiz = await create_random_quiz(session)
    await create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=True)

    res = await client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": (await quiz.get_game()).name}


async def test_get_correct_answer_with_exceed_submission_limit(
    client: AsyncClient, session: AsyncSession, current_user: User
):
    quiz = await create_random_quiz(session)
    [
        await create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=False)
        for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT)
    ]

    res = await client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert res_json == {"correct_answer": (await quiz.get_game()).name}


async def test_get_correct_answer_with_unauthorized_request(client: AsyncClient):
    quiz_id = 1

    res = await client.get(f"/quiz/correct_answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_correct_answer_with_not_existed_quiz_id(client: AsyncClient, current_user: User):
    quiz_id = 1

    res = await client.get(f"/quiz/correct_answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_get_correct_answer_with_not_completed_quiz(
    client: AsyncClient, session: AsyncSession, current_user: User
):
    quiz = await create_random_quiz(session)

    res = await client.get(f"/quiz/correct_answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_400_BAD_REQUEST
