from collections.abc import Iterable
from datetime import date
from typing import Optional

from sqlmodel import Session, select

from src.game.model import GameScreenshot
from src.quiz.model import DailyQuiz, Quiz, QuizAnswer

from .auth import create_random_user
from .game import create_random_game
from .screenshot import create_random_game_screenshot
from .utils import random_bool, random_name

QUIZ_SCREENSHOT_COUNT = 5


def create_random_quiz(session: Session, *, screenshots: list[GameScreenshot] | None = None) -> Quiz:
    if screenshots:
        assert len(screenshots) == QUIZ_SCREENSHOT_COUNT
        # 하나의 게임에만 속해 있어야 한다.
        assert len(set(s.game_id for s in screenshots)) == 1
    else:
        game = create_random_game(session)
        screenshots = [create_random_game_screenshot(session, game_id=game.id) for _ in range(5)]

    quiz = Quiz(screenshots=screenshots)

    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    return quiz


def create_random_quiz_answer(
    session: Session, *, quiz_id: int | None = None, user_id: int | None = None, correct: bool | None = None
) -> QuizAnswer:
    if quiz_id is None:
        quiz = create_random_quiz(session)
        assert quiz.id is not None
        quiz_id = quiz.id

    if user_id is None:
        user = create_random_user(session)
        assert user.id is not None
        user_id = user.id

    if correct is None:
        correct = random_bool()

    answer = random_name()

    quiz_answer = QuizAnswer(quiz_id=quiz_id, user_id=user_id, answer=answer, correct=correct)

    session.add(quiz_answer)
    session.commit()
    session.refresh(quiz_answer)

    return quiz_answer


def get_quiz_answer(
    session: Session, *, quiz_id: int | None = None, answer: str | None = None
) -> Optional[QuizAnswer]:
    stmt = select(QuizAnswer)
    if quiz_id:
        stmt = stmt.where(QuizAnswer.quiz_id == quiz_id)
    if answer:
        stmt = stmt.where(QuizAnswer.answer == answer)

    return session.exec(stmt).first()


def create_random_daily_quiz(session: Session, *, target_date: date, quiz_id: int | None = None) -> DailyQuiz:
    if quiz_id is None:
        quiz = create_random_quiz(session)
        assert quiz.id is not None
        quiz_id = quiz.id

    daily_quiz = DailyQuiz(target_date=target_date, quiz_id=quiz_id)

    session.add(daily_quiz)
    session.commit()
    session.refresh(daily_quiz)

    return daily_quiz
