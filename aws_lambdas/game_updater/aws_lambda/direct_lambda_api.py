from typing import Any, Sequence

from .. import protocols
from .event import Event
from .model import SaveGame


class DirectLambdaAPI(protocols.LambdaAPI):
    def invoke_lambda(self, event: Event) -> Any:
        from database_lambda.lambda_func import lambda_handler as database_lambda_handler

        return database_lambda_handler(event, None)

    def save_games(self, games: Sequence[SaveGame]):
        event = Event(name="save_games", payload=[g.model_dump() for g in games])
        self.invoke_lambda(event)
