from typing import Any, Collection

from sqlalchemy.orm import Session

from . import repository
from .model import GameScreenshot


def save_screenshots(session: Session, screenshots: Collection[dict[str, Any]]):
    screenshots_ = [GameScreenshot(**s) for s in screenshots]
    session.add_all(screenshots_)
    session.commit()


def get_screenshots_in_steam_file_ids(session: Session, file_ids: Collection[int]) -> list[dict[str, Any]]:
    screenshots = repository.get_game_screenshots_in_steam_file_ids(session, file_ids)

    return [s.to_dto().model_dump(mode="json") for s in screenshots]
