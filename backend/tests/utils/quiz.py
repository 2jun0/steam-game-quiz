import random
from datetime import date
from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.game.model import GameScreenshot
from src.quiz.model import DailyQuiz, Quiz, QuizAnswer

from .auth import create_random_user
from .game import create_random_game
from .screenshot import create_random_game_screenshot
from .utils import random_bool, random_name

QUIZ_SCREENSHOT_COUNT = 5


async def create_random_quiz(session: AsyncSession, *, screenshots: list[GameScreenshot] | None = None) -> Quiz:
    if screenshots:
        assert len(screenshots) == QUIZ_SCREENSHOT_COUNT
        # 하나의 게임에만 속해 있어야 한다.
        assert len(set(s.game_id for s in screenshots)) == 1
    else:
        game = await create_random_game(session)
        screenshots = [await create_random_game_screenshot(session, game_id=game.id) for _ in range(5)]

    quiz = Quiz(screenshots=screenshots)

    session.add(quiz)
    await session.commit()

    return quiz


async def create_random_quiz_answer(
    session: AsyncSession, *, quiz_id: int | None = None, user_id: int | None = None, correct: bool | None = None
) -> QuizAnswer:
    if quiz_id is None:
        quiz = await create_random_quiz(session)
        assert quiz.id is not None
        quiz_id = quiz.id

    if user_id is None:
        user = await create_random_user(session)
        assert user.id is not None
        user_id = user.id

    if correct is None:
        correct = random_bool()

    answer = random_name()

    quiz_answer = QuizAnswer(quiz_id=quiz_id, user_id=user_id, answer=answer, correct=correct)

    session.add(quiz_answer)
    await session.commit()

    return quiz_answer


async def get_quiz_answer(
    session: AsyncSession, *, quiz_id: int | None = None, answer: str | None = None
) -> Optional[QuizAnswer]:
    stmt = select(QuizAnswer)
    if quiz_id:
        stmt = stmt.where(QuizAnswer.quiz_id == quiz_id)
    if answer:
        stmt = stmt.where(QuizAnswer.answer == answer)

    return (await session.exec(stmt)).first()


async def create_random_daily_quiz(
    session: AsyncSession, *, target_date: date, quiz_id: int | None = None, feature: str | None = None
) -> DailyQuiz:
    if quiz_id is None:
        quiz = await create_random_quiz(session)
        assert quiz.id is not None
        quiz_id = quiz.id

    if feature is None:
        feature = create_random_feature()

    daily_quiz = DailyQuiz(target_date=target_date, quiz_id=quiz_id, feature=feature)

    session.add(daily_quiz)
    await session.commit()

    return daily_quiz


def create_random_feature() -> str:
    return random.choice(["Older Action", "Older Adventure", "Newer RPG", "Newer Sports"])
