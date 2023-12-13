from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from src.config import Config
from src.database import init_database
from src.logger import logger
from src.scraper.service import scrap_game_screenshot_for_all, scrap_games
from src.steam.steam_api import SteamAPI

config = Config()  # type: ignore


def scrap_games_job(engine: Engine):
    logger.info("-- scrap game job start -- ")

    with Session(engine) as session:
        scrap_games(SteamAPI(), session)
        session.commit()

    logger.info("-- scrap game job end -- ")


def scrap_screenshots_job(engine: Engine):
    logger.info("-- scrap screenshot job start -- ")

    with Session(engine) as session:
        scrap_game_screenshot_for_all(SteamAPI(), session)
        session.commit()

    logger.info("-- scrap screenshot job end -- ")


def lambda_handler(event: Any, context: Any):
    engine = create_engine(config.DATABASE_URL)
    init_database(config, engine)

    scrap_games_job(engine)
    scrap_screenshots_job(engine)
