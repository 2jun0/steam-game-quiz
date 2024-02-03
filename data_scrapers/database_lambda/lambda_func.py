from typing import Any, Callable

from sqlalchemy.orm import Session

from database_lambda.database import engine, init_database
from database_lambda.event import Event, EventName
from database_lambda.game.service import get_games_in_steam_ids, get_some_games, save_games
from database_lambda.logger import logger
from database_lambda.screenshot.service import get_screenshots_in_steam_file_ids, save_screenshots

funcs: dict[EventName, Callable[..., Any]] = {
    "save_games": save_games,
    "get_some_games": get_some_games,
    "get_games_in_steam_ids": get_games_in_steam_ids,
    "save_screenshots": save_screenshots,
    "get_screenshots_in_steam_file_ids": get_screenshots_in_steam_file_ids,
}


def handle_event(session: Session, event: Event) -> Any:
    func = funcs[event["name"]]

    try:
        result = func(session, event["payload"])
    except TypeError:
        result = func(session)

    session.commit()
    return result


def lambda_handler(event: Event, context: Any):
    init_database()

    logger.info("Handle event [required event is %s]", event)

    with Session(engine) as session:
        result = handle_event(session, event)

    logger.info("Result: %s", result)

    return result
