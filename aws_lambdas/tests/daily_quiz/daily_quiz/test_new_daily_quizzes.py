import pytest

from daily_quiz.config import setting
from daily_quiz.daily_quiz.serivce import new_daily_quizzes
from tests.daily_quiz.utils.mock_lambda_api import MockLambdaAPI
from tests.daily_quiz.utils.mock_steam_api import MockSteamAPI


@pytest.mark.parametrize("setting_quiz_cnt", (5, 10))
def test_new_daily_quizzes는_설정값만큼_데일리_퀴즈를_만들어야한다(setting_quiz_cnt: int):
    setting.DAILY_QUIZ_CNT = setting_quiz_cnt
    lambda_api = MockLambdaAPI()
    steam_api = MockSteamAPI()

    new_daily_quizzes(lambda_api, steam_api)

    assert len(lambda_api.daily_quizzes) == setting_quiz_cnt
