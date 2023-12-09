from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database import init_database

from .config import Config
from .scraper.service import scrap_game_screenshot_for_all, scrap_games
from .steam.steam_api import SteamAPI

scheduler = BlockingScheduler()

config = Config()  # type: ignore
engine = create_engine(config.DATABASE_URL)
init_database(config, engine)


@scheduler.scheduled_job(CronTrigger.from_crontab("0 3 * * *"), id="scrap_games_job")
def scrap_games_job():
    with Session(engine) as session:
        scrap_games(SteamAPI(), session)
        session.commit()


@scheduler.scheduled_job(CronTrigger.from_crontab("0 3 * * *"), id="scrap_screenshots_job")
def scrap_screenshots_job():
    with Session(engine) as session:
        scrap_game_screenshot_for_all(SteamAPI(), session)
        session.commit()


scheduler.start()
