import random
from collections.abc import Iterable

from daily_quiz.aws_lambda.model import Game, SaveDailyQuiz, SaveGameScreenshot, SaveQuiz
from daily_quiz.config import setting
from daily_quiz.protocols import LambdaAPI
from tests.daily_quiz.utils.model import create_random_game


class MockLambdaAPI(LambdaAPI):
    def __init__(self) -> None:
        self.games = []
        for k in range(1, 4):
            self.games.extend(
                [create_random_game(genres=random.sample(setting.GAME_GENERES, k=k)) for i in range(100)]
            )
        self.quizzes = []
        self.daily_quizzes = []

    def save_quizzes(self, quizzes: Iterable[SaveQuiz]):
        self.quizzes.extend(quizzes)

    def get_all_games(self) -> list[Game]:
        return self.games

    def save_screenshots(self, screenshots: Iterable[SaveGameScreenshot]):
        pass

    def save_daily_quizzes(self, daily_quizzes: Iterable[SaveDailyQuiz]):
        self.daily_quizzes.extend(daily_quizzes)
