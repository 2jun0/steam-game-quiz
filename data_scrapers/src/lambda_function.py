from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .config import Config
from .database import init_database
from .scraper.service import scrap_game_screenshot_for_all, scrap_games
from .steam.steam_api import SteamAPI

config = Config()  # type: ignore
engine = create_engine(config.DATABASE_URL)
init_database(config, engine)


def scrap_games_job():
    with Session(engine) as session:
        scrap_games(SteamAPI(), session)
        session.commit()


def scrap_screenshots_job():
    with Session(engine) as session:
        scrap_game_screenshot_for_all(SteamAPI(), session)
        session.commit()


def lambda_handler(event: Any, context: Any):
    scrap_games_job()
    scrap_screenshots_job()
