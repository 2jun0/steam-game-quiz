from collections.abc import Iterable
from typing import TypedDict

from sqlalchemy.orm import Session

from . import repository
from .model import GameScreenshot

STEAM_FILE_ID = int


class SaveGameScreenshot(TypedDict):
    steam_file_id: STEAM_FILE_ID
    url: str
    game_id: int


def _attach_models(session: Session, models: dict[STEAM_FILE_ID, GameScreenshot]):
    saved = repository.get_game_screenshots_in_steam_file_ids(session, models.keys())

    for s in saved:
        query = models[s.steam_file_id]
        s.url = query.url
        s.game_id = query.game_id
        models[s.steam_file_id] = s


def _to_models(screenshots: Iterable[SaveGameScreenshot]):
    models: dict[STEAM_FILE_ID, GameScreenshot] = {}
    for screenshot in screenshots:
        models[screenshot["steam_file_id"]] = GameScreenshot(**screenshot)

    return models


def save_screenshots(session: Session, screenshots: Iterable[SaveGameScreenshot]):
    # turn to model
    models = _to_models(screenshots)

    # detached된 객체의 식별자 업데이트
    _attach_models(session, models)

    session.add_all(models.values())
