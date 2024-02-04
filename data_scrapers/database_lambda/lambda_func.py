from typing import Any, Callable

from sqlalchemy.orm import Session

from database_lambda.database import engine, init_database
from database_lambda.event import Event, EventName
from database_lambda.game.service import save_games
from database_lambda.logger import logger
from database_lambda.screenshot.service import save_screenshots

funcs: dict[EventName, Callable[..., Any]] = {
    "save_games": save_games,
    "save_screenshots": save_screenshots,
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
