import pytest
from pytest_factoryboy import register
from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import drop_database  # type: ignore

from private.config import Config
from private.database import init_database
from private.game.model import Game
from private.screenshot.model import GameScreenshot
from tests.private import database
from tests.private.config import TestConfig
from tests.private.factories import GameFactory, GameScreenshotFactory

register(GameFactory)
register(GameScreenshotFactory)


@pytest.fixture(scope="session")
def config() -> Config:
    return TestConfig()  # type: ignore


@pytest.fixture(scope="session")
def engine(config: Config):
    engine = create_engine(config.DATABASE_URL)

    init_database(config, engine)

    database.Session.configure(bind=engine)
    yield engine
    drop_database(config.DATABASE_URL)
    engine.dispose()


@pytest.fixture()
def session(engine: Engine):
    with database.Session() as session:
        yield session


@pytest.fixture()
def mock_session():
    return


@pytest.fixture
def saved_games() -> list[Game]:
    return GameFactory.create_batch(100)


@pytest.fixture
def saved_screenshots() -> list[GameScreenshot]:
    return GameScreenshotFactory.create_batch(100)
