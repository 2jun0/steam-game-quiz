from collections.abc import Iterable
from datetime import date, timedelta

from ..aws_lambda.model import Game, SaveDailyQuiz, SaveQuiz
from ..config import setting
from ..protocols import LambdaAPI, SteamAPI
from .game_picker import pick_games
from .genre_picker import pick_genres
from .screenshot_scraper import scrap_screenshots
from .utils import utc_today


def create_quizzes(steam_api: SteamAPI, games: Iterable[Game]) -> list[SaveQuiz]:
    quizzes = []
    for game in games:
        # 스크린샷 크롤링
        screenshots = scrap_screenshots(steam_api, game)
        quizzes.append(SaveQuiz(screenshots=screenshots))

    return quizzes


def create_daily_quizzes(target_date: date, quizzes: Iterable[SaveQuiz]) -> list[SaveDailyQuiz]:
    return [SaveDailyQuiz(quiz=quiz, target_date=target_date) for quiz in quizzes]


def new_daily_quizzes(lambda_api: LambdaAPI, steam_api: SteamAPI):
    # 모든 게임 가져오기
    all_games = lambda_api.get_all_games()

    # 장르 선택
    picked_genres = pick_genres(setting.DAILY_QUIZ_CNT)

    # 게임 선택
    picked_games = pick_games(all_games, picked_genres)

    # 퀴즈 생성 (스크린샷 스크래핑함)
    quizzes = create_quizzes(steam_api, picked_games)

    # 데일리 퀴즈 생성 (퀴즈 스크래핑함)
    utc_tomorrow = utc_today() + timedelta(days=1)
    daily_quizzes = create_daily_quizzes(utc_tomorrow, quizzes)

    # 저장
    lambda_api.save_daily_quizzes(daily_quizzes)
