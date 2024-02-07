import random

from ..config import setting


def pick_genres(k: int) -> list[str]:
    return random.choices(setting.GAME_GENERES, k=k)
