from typing import Any, Callable

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from private.config import Config
from private.database import init_database
from private.event import Event, EventName
from private.game.service import get_games_in_steam_ids, get_some_games, save_games
from private.logger import logger
from private.screenshot.service import get_screenshots_in_steam_file_ids, save_screenshots

config = Config()  # type: ignore

funcs: dict[EventName, Callable[..., Any]] = {
    "save_games": save_games,
    "get_some_games": get_some_games,
    "get_games_in_steam_ids": get_games_in_steam_ids,
    "save_screenshots": save_screenshots,
    "get_screenshots_in_steam_file_ids": get_screenshots_in_steam_file_ids,
}


def handle_event(engine: Engine, event: Event) -> Any:
    with Session(engine) as session:
        func = funcs[event["name"]]

        try:
            result = func(session, event["payload"])
        except TypeError:
            result = func(session)

        session.commit()
        return result


def lambda_handler(event: Event, context: Any):
    engine = create_engine(config.DATABASE_URL)
    init_database(config, engine)

    logger.info("Handle event [required event is %s]", event)

    result = handle_event(engine, event)

    logger.info("Result: %s", result)

    return result
