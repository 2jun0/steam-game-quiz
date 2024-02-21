import pytest

from daily_quiz.config import setting
from daily_quiz.daily_quiz.serivce import create_quizzes
from tests.daily_quiz.utils.mock_steam_api import MockSteamAPI
from tests.daily_quiz.utils.model import create_random_game


@pytest.mark.parametrize("game_cnt", (0, 5, 10))
def test_create_quizzes는_게임_개수만큼_퀴즈를_만들어야한다(game_cnt: int):
    games = {f"feature-{i}": create_random_game() for i in range(game_cnt)}
    steam_api = MockSteamAPI()

    quizzes = create_quizzes(steam_api, games)

    assert len(quizzes) == game_cnt


@pytest.mark.parametrize("screenshot_cnt", (0, 5, 10))
def test_create_quizzes는_퀴즈별로_설정값만큼_스크린샷을_할당해야_한다(screenshot_cnt: int):
    setting.QUIZ_SCREENSHOT_CNT = screenshot_cnt
    games = {f"feature-{i}": create_random_game() for i in range(5)}
    steam_api = MockSteamAPI()

    quizzes = create_quizzes(steam_api, games)
    for quiz in quizzes.values():
        assert len(quiz.screenshots) == screenshot_cnt
