# type: ignore
from datetime import datetime

import factory
from factory.alchemy import SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText

from private.game.model import Game
from private.screenshot.model import GameScreenshot
from tests.private.database import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH


class GameFactory(BaseFactory):
    class Meta:
        model = Game

    id = factory.Sequence(lambda num: num)
    steam_id = factory.Sequence(lambda num: num)
    name = factory.Sequence(lambda num: f"game{num}")
    kr_name = factory.Sequence(lambda num: f"게임{num}")
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


class GameScreenshotFactory(BaseFactory):
    class Meta:
        model = GameScreenshot

    id = factory.Sequence(lambda num: num)
    steam_file_id = factory.Sequence(lambda num: num)
    url = FuzzyText("https://fake.com/url", 100)

    game = factory.LazyFunction(GameFactory.create)
    game_id = factory.LazyAttribute(lambda s: s.game.id)

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)
