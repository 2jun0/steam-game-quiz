import pytest

from daily_quiz.config import setting
from daily_quiz.daily_quiz.genre_picker import pick_genres


@pytest.mark.parametrize("setting_quiz_cnt", (5, 10))
def test_pick_genres는_퀴즈의_개수만큼_장르를_반환해야_한다(setting_quiz_cnt: int):
    setting.DAILY_QUIZ_CNT = setting_quiz_cnt
    genres = pick_genres()

    assert len(genres) == setting.DAILY_QUIZ_CNT


@pytest.mark.parametrize("setting_genres", (tuple(setting.GAME_GENERES), ("Adventure", "RPG")))
def test_pick_genres는_설정값에서_장르를_선택해야_한다(setting_genres: tuple[str]):
    setting.GAME_GENERES = setting_genres
    genres = pick_genres()

    assert set(setting.GAME_GENERES) == set(genres) | set(setting.GAME_GENERES)
