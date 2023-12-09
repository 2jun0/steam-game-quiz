from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.scraper.model import Game, GameScreenshot
from src.scraper.protocols import SteamAPI
from src.scraper.service import scrap_game_screenshot, scrap_games
from src.steam.model import SteamGameDetailResponse, SteamGameScreenshotResponse, TopSteamGameResponse
from tests.factories import (
    SteamGameDetailResponseFactory,
    SteamGameScreenshotResponseFactory,
    TopSteamGameResponseFactory,
)


class MockSteamAPI(SteamAPI):
    def __init__(self) -> None:
        TopSteamGameResponseFactory.reset_sequence()
        SteamGameDetailResponseFactory.reset_sequence()
        SteamGameScreenshotResponseFactory.reset_sequence()

    def get_top_100_games_in_2weeks(self) -> list[TopSteamGameResponse]:
        return TopSteamGameResponseFactory.build_batch(100)

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        return SteamGameDetailResponseFactory.build()

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        return SteamGameScreenshotResponseFactory.build_batch(10)


def test_scrap_geams는_100개의_게임을_저장한다(session: Session):
    scrap_games(MockSteamAPI(), session)

    scraped = session.scalars(select(Game)).all()

    assert len(scraped) == 100


def test_scrap_games는_중복된_게임은_다시_저장하지_않는다(session: Session):
    scrap_games(MockSteamAPI(), session)
    scrap_games(MockSteamAPI(), session)  # duplicated

    scraped = session.scalars(select(Game)).all()

    assert len(scraped) == 100


def test_scrap_screenshots은_스크린샷을_저장한다(session: Session, game: Game):
    scrap_game_screenshot(MockSteamAPI(), session, game)

    scraped = session.scalars(statement=select(GameScreenshot)).all()

    assert len(scraped) > 0


def test_scrap_screenshot은_중복된_스크린샷은_다시_저장하지_않는다(session: Session, game: Game):
    scrap_game_screenshot(MockSteamAPI(), session, game)
    before_scraped = session.scalars(statement=select(GameScreenshot)).all()

    scrap_game_screenshot(MockSteamAPI(), session, game)
    after_scraped = session.scalars(statement=select(GameScreenshot)).all()

    assert len(before_scraped) == len(after_scraped)
