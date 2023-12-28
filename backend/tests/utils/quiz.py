import asyncio

from sqlmodel import Session

from src.database import engine
from src.game.model import GameScreenshot
from src.quiz.model import Quiz

from .game import create_random_game
from .screenshot import create_random_game_screenshot

QUIZ_SCREENSHOT_COUNT = 5


async def create_random_quiz(screenshots: list[GameScreenshot] | None = None) -> Quiz:
    if screenshots:
        assert len(screenshots) == QUIZ_SCREENSHOT_COUNT
        # 하나의 게임에만 속해 있어야 한다.
        assert len(set(s.game_id for s in screenshots)) == 1
    else:
        game = await create_random_game()
        screenshots = await asyncio.gather(*[create_random_game_screenshot(game.id) for _ in range(5)])

    with Session(engine) as session:
        quiz = Quiz(screenshots=screenshots)

        session.add(quiz)
        session.commit()
        session.refresh(quiz, ["screenshots"])

    return quiz
