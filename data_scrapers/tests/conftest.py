import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database  # type: ignore

from src.config import Config
from src.database import init_database
from src.scraper.model import Game
from tests import database
from tests.config import TestConfig
from tests.factories import GameFactory


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
def game(session: Session) -> Game:
    return GameFactory()  # type: ignore


@pytest.fixture
def games(session: Session) -> list[Game]:
    return [GameFactory(), GameFactory()]  # type: ignore
