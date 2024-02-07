import random
from typing import Sequence

from daily_quiz.aws_lambda.model import Game, SaveGameScreenshot, SaveQuiz
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

    def save_quizzes(self, quizzes: Sequence[SaveQuiz]):
        self.quizzes.extend(quizzes)

    def get_all_games(self) -> list[Game]:
        return self.games

    def save_screenshots(self, screenshots: Sequence[SaveGameScreenshot]):
        pass
