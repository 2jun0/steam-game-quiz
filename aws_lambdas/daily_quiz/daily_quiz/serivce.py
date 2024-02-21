import random
from datetime import date, timedelta

from ..aws_lambda.model import Game, SaveDailyQuiz, SaveQuiz
from ..config import setting
from ..protocols import LambdaAPI, SteamAPI
from .game_picker import FEATURE, pick_games
from .genre_picker import pick_genres
from .screenshot_scraper import scrap_screenshots
from .utils import utc_today


def create_quizzes(steam_api: SteamAPI, games: dict[FEATURE, Game]) -> dict[FEATURE, SaveQuiz]:
    quizzes: dict[FEATURE, SaveQuiz] = {}
    for feature, game in games.items():
        # 스크린샷 크롤링
        screenshots = scrap_screenshots(steam_api, game)
        quiz_screenshots = random.sample(screenshots, k=setting.QUIZ_SCREENSHOT_CNT)
        quizzes[feature] = SaveQuiz(screenshots=quiz_screenshots)

    return quizzes


def create_daily_quizzes(target_date: date, quizzes: dict[FEATURE, SaveQuiz]) -> list[SaveDailyQuiz]:
    return [SaveDailyQuiz(quiz=quiz, target_date=target_date, feature=feature) for feature, quiz in quizzes.items()]


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
