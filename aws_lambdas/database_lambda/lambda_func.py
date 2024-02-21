from typing import Any, Protocol, Union, cast


def lambda_handler(event: Any, context: Any):

    from elasticsearch import Elasticsearch
    from sqlalchemy.orm import Session

    from database_lambda.database import engine
    from database_lambda.es import es_client
    from database_lambda.event import Event, EventName
    from database_lambda.game.service import get_all_games, save_games
    from database_lambda.logger import logger
    from database_lambda.quiz.service import save_daily_quizzes, save_quizzes
    from database_lambda.screenshot.service import save_screenshots

    class NoPayloadEventHandler(Protocol):
        def __call__(self, *, session: Session, es_client: Elasticsearch, **kwargs) -> Any: ...

    class PayloadEventHandler(Protocol):
        def __call__(self, __payload, *, session: Session, es_client: Elasticsearch, **kwargs) -> Any: ...

    funcs: dict[EventName, Union[NoPayloadEventHandler, PayloadEventHandler]] = {
        "save_games": save_games,
        "save_screenshots": save_screenshots,
        "get_all_games": get_all_games,
        "save_quizzes": save_quizzes,
        "save_daily_quizzes": save_daily_quizzes,
    }

    def handle_event(session: Session, event: Event) -> Any:
        func = funcs[event["name"]]

        if "payload" in event and event["payload"]:
            func = cast(PayloadEventHandler, func)
            result = func(event["payload"], session=session, es_client=es_client)
        else:
            func = cast(NoPayloadEventHandler, func)
            result = func(session=session, es_client=es_client)

        session.commit()
        return result

    logger.info("Handle event [required event is %s]", event)

    with Session(engine) as session:
        result = handle_event(session, event)

    logger.info("Result: %s", result)

    return result
