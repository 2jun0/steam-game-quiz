from sqlalchemy import create_engine

from .config import test_settings

engine = create_engine(test_settings.TEST_DATABASE_URL, echo=True)  # type: ignore
