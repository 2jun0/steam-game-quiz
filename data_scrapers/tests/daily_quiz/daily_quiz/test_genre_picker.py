import pytest

from daily_quiz.config import setting
from daily_quiz.daily_quiz.genre_picker import pick_genres


@pytest.mark.parametrize("genre_cnt", (5, 10))
def test_pick_genres는_입력된_개수만큼_유일한_장르_개수를_반환해야_한다(genre_cnt: int):
    genres = pick_genres(genre_cnt)

    assert len(set(genres)) == genre_cnt


@pytest.mark.parametrize("setting_genres", (tuple(setting.GAME_GENERES), ("Adventure", "RPG")))
@pytest.mark.parametrize("genre_cnt", (5, 10))
def test_pick_genres는_설정값에서_장르를_선택해야_한다(genre_cnt: int, setting_genres: tuple[str]):
    setting.GAME_GENERES = setting_genres
    genres = pick_genres(genre_cnt)

    assert set(setting.GAME_GENERES) == set(genres) | set(setting.GAME_GENERES)
