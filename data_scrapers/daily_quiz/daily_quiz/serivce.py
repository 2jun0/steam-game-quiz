from typing import Iterable

from ..aws_lambda.model import Game, SaveQuiz
from ..protocols import LambdaAPI, SteamAPI
from .game_picker import pick_games
from .genre_picker import pick_genres
from .screenshot_scraper import scrap_screenshots


def create_quizzes(steam_api: SteamAPI, games: Iterable[Game]) -> list[SaveQuiz]:
    quizzes = []
    for game in games:
        # 스크린샷 크롤링
        screenshots = scrap_screenshots(steam_api, game)
        quizzes.append(SaveQuiz(screenshots=screenshots))

    return quizzes


def new_daily_quizzes(lambda_api: LambdaAPI, steam_api: SteamAPI):
    # 모든 게임 가져오기
    all_games = lambda_api.get_all_games()

    # 장르 선택
    picked_genres = pick_genres()

    # 게임 선택
    picked_games = pick_games(all_games, picked_genres)

    # 퀴즈 생성 (스크린샷 스크래핑함)
    quizzes = create_quizzes(steam_api, picked_games)

    # 저장
    lambda_api.save_quizzes(quizzes)
