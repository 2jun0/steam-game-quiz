from collections.abc import Iterable

from sqlalchemy.orm import Session

from .model_factory import to_models
from .schema import SaveGameScreenshot


def save_screenshots(screenshots: Iterable[SaveGameScreenshot], *, session: Session, **kwargs):
    models = to_models(session, screenshots)
    session.add_all(models)
