import random

from ..config import setting


def pick_genres() -> list[str]:
    return random.choices(setting.GAME_GENERES, k=5)
