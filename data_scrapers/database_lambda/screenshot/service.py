from typing import Any, Collection

from sqlalchemy.orm import Session

from .model import GameScreenshot


def save_screenshots(session: Session, screenshots: Collection[dict[str, Any]]):
    screenshots_ = [GameScreenshot(**s) for s in screenshots]
    session.add_all(screenshots_)
