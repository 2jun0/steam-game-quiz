from sqlmodel import Session

from src.game.model import GameScreenshot
from src.quiz.model import Quiz

from .game import create_random_game
from .screenshot import create_random_game_screenshot

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
