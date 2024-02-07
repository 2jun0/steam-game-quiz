from collections.abc import Iterable

from sqlalchemy.orm import Session

from . import repository
from .model import GameScreenshot
from .schema import STEAM_FILE_ID, SaveGameScreenshot


def _attach_models(session: Session, models: dict[STEAM_FILE_ID, GameScreenshot]):
    saved = repository.get_game_screenshots_in_steam_file_ids(session, models.keys())

    for s in saved:
        query = models[s.steam_file_id]
        s.url = query.url
        s.game_id = query.game_id
        models[s.steam_file_id] = s


def _create_models(screenshots: Iterable[SaveGameScreenshot]) -> dict[STEAM_FILE_ID, GameScreenshot]:
    models: dict[STEAM_FILE_ID, GameScreenshot] = {}
    for screenshot in screenshots:
        models[screenshot["steam_file_id"]] = GameScreenshot(**screenshot)

    return models


def to_models(session: Session, screenshots: Iterable[SaveGameScreenshot]) -> list[GameScreenshot]:
    models = _create_models(screenshots)
    # detached된 객체의 식별자 업데이트
    _attach_models(session, models)

    return list(models.values())
