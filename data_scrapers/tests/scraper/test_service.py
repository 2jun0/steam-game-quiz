from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.scraper.model import Game
from src.scraper.protocols import SteamAPI
from src.scraper.service import scrap_games
from src.steam.model import SteamGameDetailResponse, SteamGameScreenshotResponse, TopSteamGameResponse
from tests.factories import (
    SteamGameDetailResponseFactory,
    SteamGameScreenshotResponseFactory,
    TopSteamGameResponseFactory,
)


class MockSteamAPI(SteamAPI):
    def __init__(self) -> None:
        self.top_100_games = TopSteamGameResponseFactory.build_batch(100)

    def get_top_100_games_in_2weeks(self) -> list[TopSteamGameResponse]:
        return self.top_100_games

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        return SteamGameDetailResponseFactory.build()

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        return SteamGameScreenshotResponseFactory.build_batch(10)


def test_scrap_geams는_100개의_게임을_저장한다(session: Session):
    scrap_games(MockSteamAPI(), session)

    scraped = session.scalars(select(Game)).all()

    assert len(scraped) == 100


def test_scrap_games는_중복된_게임은_다시_저장하지_않는다(session: Session) -> None:
    steam_api = MockSteamAPI()

    scrap_games(steam_api, session)
    scrap_games(steam_api, session)  # duplicated

    scraped = session.scalars(select(Game)).all()

    assert len(scraped) == 100
