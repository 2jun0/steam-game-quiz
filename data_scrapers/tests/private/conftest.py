import pytest
from pytest_factoryboy import register
from sqlalchemy.orm import Session

from private.game.model import Game
from private.screenshot.model import GameScreenshot
from tests.private.database import Session as _Session
from tests.private.database import drop_tables, engine, init_database
from tests.private.factories import GameFactory, GameScreenshotFactory

register(GameFactory)
register(GameScreenshotFactory)


@pytest.fixture(autouse=True)
def database():
    init_database()
    yield
    drop_tables()
    engine.dispose()


@pytest.fixture
def session() -> Session:
    return _Session()


@pytest.fixture
def saved_games() -> list[Game]:
    return GameFactory.create_batch(100)


@pytest.fixture
def saved_screenshots() -> list[GameScreenshot]:
    return GameScreenshotFactory.create_batch(100)
