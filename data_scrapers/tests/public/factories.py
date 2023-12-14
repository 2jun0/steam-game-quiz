# type: ignore

from datetime import datetime

import factory
from factory.fuzzy import FuzzyText
from pytest_factoryboy import register

from public.model import (
    Game,
    GameScreenshot,
    SteamFeatureGameResponse,
    SteamGameDetailResponse,
    SteamGameScreenshotResponse,
)


class SteamFeatureGameResponseFactory(factory.Factory):
    class Meta:
        model = SteamFeatureGameResponse

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


@register
class GameFactory(factory.Factory):
    class Meta:
        model = Game

    id = factory.Sequence(lambda n: n)
    steam_id = factory.Sequence(lambda n: n)
    name = FuzzyText(100)
    kr_name = FuzzyText(100)
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


class GameScreenshotFactory(factory.Factory):
    class Meta:
        model = GameScreenshot

    id = factory.Sequence(lambda n: n)
    steam_file_id = factory.Sequence(lambda n: n)
    url = FuzzyText("https://fake.com/url", 100)
    game_id = 0
    game = Game(
        id=0, steam_id=0, name="Default", kr_name="Default", updated_at=datetime.utcnow(), created_at=datetime.utcnow()
    )
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)
