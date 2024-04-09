from fastapi import status
from httpx import AsyncClient, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.model import User
from src.config import settings
from tests.utils.quiz import create_random_quiz, create_random_quiz_answer, get_quiz_answer


async def test_post_submit_true_answer(client: AsyncClient, session: AsyncSession, current_user: User):
    saved_quiz = await create_random_quiz(session)

    res = await client.post(
        "/quiz/submit_answer", json={"quiz_id": saved_quiz.id, "answer": (await saved_quiz.get_game()).name}
    )
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is True

    # check db
    submit = await get_quiz_answer(session, quiz_id=saved_quiz.id)
    assert submit is not None
    assert submit.correct is True
    assert submit.user_id == current_user.id


async def test_post_submit_false_answer(client: AsyncClient, session: AsyncSession, current_user: User):
    saved_quiz = await create_random_quiz(session)

    res = await client.post("/quiz/submit_answer", json={"quiz_id": saved_quiz.id, "answer": "빙빙바리바리구"})
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["correct"] is False

    # check db
    submit = await get_quiz_answer(session, quiz_id=saved_quiz.id)
    assert submit is not None
    assert submit.correct is False
    assert submit.user_id == current_user.id


async def test_post_submit_answer_with_not_existed_quiz_id(client: AsyncClient, current_user: User):
    res = await client.post("/quiz/submit_answer", json={"quiz_id": -1, "answer": "아무거나 빙빙바리바리구"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_post_submit_answer_with_unauthorized_request(client: AsyncClient):
    res = await client.post("/quiz/submit_answer", json={"quiz_id": -1, "answer": "아무거나 빙빙바리바리구"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_post_submit_answer_with_exceed_submission_limit(
    client: AsyncClient, session: AsyncSession, current_user: User
):
    quiz = await create_random_quiz(session)
    _ = [
        await create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=False)
        for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT)
    ]

    res: Response = await client.post("/quiz/submit_answer", json={"quiz_id": quiz.id, "answer": "아무거나 방방빙방"})
    assert res.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_submit_answer_with_prior_correct_answer(
    client: AsyncClient, session: AsyncSession, current_user: User
):
    quiz = await create_random_quiz(session)
    await create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id, correct=True)

    res = await client.post("/quiz/submit_answer", json={"quiz_id": quiz.id, "answer": "아무거나 방방빙방"})
    assert res.status_code == status.HTTP_400_BAD_REQUEST
