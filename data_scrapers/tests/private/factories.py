# type: ignore
from datetime import datetime

import factory
from factory.alchemy import SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory

from private.game.model import Game
from tests.private.database import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH


class GameFactory(BaseFactory):
    class Meta:
        model = Game

    steam_id = factory.Sequence(lambda num: num)
    name = factory.Sequence(lambda num: f"game{num}")
    kr_name = factory.Sequence(lambda num: f"게임{num}")
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)
