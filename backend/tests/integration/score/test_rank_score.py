import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.model import User
from src.config import settings
from tests.utils.quiz import create_random_quiz


@pytest.mark.parametrize("score_diff_on_correct_first", (0, 1, settings.SCORE_DIFF_ON_CORRECT_FIRST, 100))
async def test_complete_quiz_on_correct_first(
    client: AsyncClient, session: AsyncSession, current_user: User, score_diff_on_correct_first: int
):
    settings.SCORE_DIFF_ON_CORRECT_FIRST = score_diff_on_correct_first
    before_score = current_user.rank_score
    quiz = await create_random_quiz(session)
    game = await quiz.get_game()

    res = await client.post("/quiz/submit_answer", json={"quiz_id": quiz.id, "answer": game.name})
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["correct"] is True

    assert current_user.rank_score - before_score == settings.SCORE_DIFF_ON_CORRECT_FIRST


@pytest.mark.parametrize("score_diff_on_correct_repeat", (0, 1, settings.SCORE_DIFF_ON_CORRECT_REPEAT, 100))
async def test_complete_quiz_on_correct_repeat(
    client: AsyncClient, session: AsyncSession, current_user: User, score_diff_on_correct_repeat: int
):
    settings.SCORE_DIFF_ON_CORRECT_REPEAT = score_diff_on_correct_repeat
    quiz1 = await create_random_quiz(session)
    quiz2 = await create_random_quiz(session, screenshots=await quiz1.awt_screenshots)
    game = await quiz1.get_game()

    res1 = await client.post("/quiz/submit_answer", json={"quiz_id": quiz1.id, "answer": game.name})
    assert res1.status_code == status.HTTP_200_OK
    assert res1.json()["correct"] is True
    before_score = current_user.rank_score

    res2 = await client.post("/quiz/submit_answer", json={"quiz_id": quiz2.id, "answer": game.name})
    assert res2.status_code == status.HTTP_200_OK
    assert res2.json()["correct"] is True

    assert current_user.rank_score - before_score == settings.SCORE_DIFF_ON_CORRECT_REPEAT


@pytest.mark.parametrize("score_diff_on_failed", (0, -1, settings.SCORE_DIFF_ON_FAILED, -100))
async def test_complete_quiz_on_failed(
    client: AsyncClient, session: AsyncSession, current_user: User, score_diff_on_failed: int
):
    settings.SCORE_DIFF_ON_FAILED = score_diff_on_failed
    current_user.rank_score = 10000
    before_score = current_user.rank_score
    quiz = await create_random_quiz(session)

    for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT):
        res = await client.post("/quiz/submit_answer", json={"quiz_id": quiz.id, "answer": "빙빙바리바리구"})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["correct"] is False

    assert current_user.rank_score - before_score == settings.SCORE_DIFF_ON_FAILED


@pytest.mark.parametrize("score_diff_on_failed", (-1, settings.SCORE_DIFF_ON_FAILED, -100))
async def test_complete_quiz_on_failed_with_underflow(
    client: AsyncClient, session: AsyncSession, current_user: User, score_diff_on_failed: int
):
    settings.SCORE_DIFF_ON_FAILED = score_diff_on_failed
    current_user.rank_score = 0
    quiz = await create_random_quiz(session)

    for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT):
        res = await client.post("/quiz/submit_answer", json={"quiz_id": quiz.id, "answer": "빙빙바리바리구"})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["correct"] is False

    assert current_user.rank_score == 0


@pytest.mark.parametrize(
    "score_diff_on_failed_after_prev_solved", (0, -1, settings.SCORE_DIFF_ON_FAILED_AFTER_PREV_SOLVED, -100)
)
async def test_complete_quiz_on_failed_after_prev_solved(
    client: AsyncClient, session: AsyncSession, current_user: User, score_diff_on_failed_after_prev_solved: int
):
    settings.SCORE_DIFF_ON_FAILED_AFTER_PREV_SOLVED = score_diff_on_failed_after_prev_solved
    quiz1 = await create_random_quiz(session)
    quiz2 = await create_random_quiz(session, screenshots=await quiz1.awt_screenshots)
    game = await quiz1.get_game()

    res1 = await client.post("/quiz/submit_answer", json={"quiz_id": quiz1.id, "answer": game.name})
    assert res1.status_code == status.HTTP_200_OK
    assert res1.json()["correct"] is True

    current_user.rank_score = 10000
    before_score = current_user.rank_score

    for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT):
        res = await client.post("/quiz/submit_answer", json={"quiz_id": quiz2.id, "answer": "빙빙바리바리구"})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["correct"] is False

    assert current_user.rank_score - before_score == settings.SCORE_DIFF_ON_FAILED_AFTER_PREV_SOLVED


@pytest.mark.parametrize(
    "score_diff_on_failed_after_prev_solved", (-1, settings.SCORE_DIFF_ON_FAILED_AFTER_PREV_SOLVED, -100)
)
async def test_complete_quiz_on_failed_after_prev_solved_with_underflow(
    client: AsyncClient, session: AsyncSession, current_user: User, score_diff_on_failed_after_prev_solved: int
):
    settings.SCORE_DIFF_ON_FAILED_AFTER_PREV_SOLVED = score_diff_on_failed_after_prev_solved
    quiz1 = await create_random_quiz(session)
    quiz2 = await create_random_quiz(session, screenshots=await quiz1.awt_screenshots)
    game = await quiz1.get_game()

    res1 = await client.post("/quiz/submit_answer", json={"quiz_id": quiz1.id, "answer": game.name})
    assert res1.status_code == status.HTTP_200_OK
    assert res1.json()["correct"] is True

    current_user.rank_score = 0

    for _ in range(settings.QUIZ_ANSWER_SUBMISSION_LIMIT):
        res = await client.post("/quiz/submit_answer", json={"quiz_id": quiz2.id, "answer": "빙빙바리바리구"})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["correct"] is False

    assert current_user.rank_score == 0
