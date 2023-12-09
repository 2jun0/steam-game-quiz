# type: ignore
from datetime import datetime

import factory
from factory.alchemy import SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText
from pytest_factoryboy import register

from src.scraper.model import Game
from src.steam.model import SteamGameDetailResponse, SteamGameScreenshotResponse, TopSteamGameResponse
from tests.database import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH


@register
class GameFactory(BaseFactory):
    class Meta:
        model = Game

    steam_id = factory.Sequence(lambda num: num)
    name = factory.Sequence(lambda num: f"game{num}")
    kr_name = factory.Sequence(lambda num: f"게임{num}")
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


class TopSteamGameResponseFactory(factory.Factory):
    class Meta:
        model = TopSteamGameResponse

    app_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"game{n}")


class SteamGameDetailResponseFactory(factory.Factory):
    class Meta:
        model = SteamGameDetailResponse

    name = factory.Sequence(lambda n: f"game{n}")


class SteamGameScreenshotResponseFactory(factory.Factory):
    class Meta:
        model = SteamGameScreenshotResponse

    file_id = factory.Sequence(lambda n: n)
    full_image_url = FuzzyText("https://fake.com/url", 100)
