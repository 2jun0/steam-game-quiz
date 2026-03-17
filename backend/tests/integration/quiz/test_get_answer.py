from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.model import User
from tests.utils.quiz import create_random_quiz, create_random_quiz_answer
from tests.utils.utils import jsontime2datetime


async def test_get_answer(session: AsyncSession, client: AsyncClient, current_user: User):
    quiz = await create_random_quiz(session)
    quiz_answer1 = await create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id)
    quiz_answer2 = await create_random_quiz_answer(session, quiz_id=quiz.id, user_id=current_user.id)

    res = await client.get(f"/quiz/answer?quiz_id={quiz.id}")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    # 제출(저장) 순서도 동일해야 한다.
    for quiz_ans_res, quiz_ans in zip(res_json["quiz_answers"], [quiz_answer1, quiz_answer2]):
        assert quiz_ans_res["answer"] == quiz_ans.answer
        assert quiz_ans_res["correct"] == quiz_ans.correct
        assert jsontime2datetime(quiz_ans_res["created_at"]) == quiz_ans.created_at


async def test_get_answer_with_not_existed_quiz_id(client: AsyncClient, current_user: User):
    quiz_id = 1

    res = await client.get(f"/quiz/answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


async def test_get_answer_with_unauthorized_request(client: AsyncClient):
    quiz_id = 1

    res = await client.get(f"/quiz/answer?quiz_id={quiz_id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
