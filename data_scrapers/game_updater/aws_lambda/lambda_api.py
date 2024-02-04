import json
from typing import Any, Sequence

import boto3

from .. import protocols
from ..config import setting
from .event import Event
from .exception import AWSLambdaException
from .model import SaveGame


class LambdaAPI(protocols.LambdaAPI):
    def __init__(self) -> None:
        self.client = boto3.client("lambda")

    def invoke_lambda(self, event: Event) -> Any:
        response = self.client.invoke(FunctionName=setting.DATABASE_LAMBDA_NAME, Payload=json.dumps(event))

        if "FunctionError" in response:
            raise AWSLambdaException(response["FunctionError"])

        payload: Any = response["Payload"].read().decode("utf-8")
        return json.loads(payload)

    def save_games(self, games: Sequence[SaveGame]):
        event = Event(name="save_games", payload=[g.model_dump() for g in games])

        self.invoke_lambda(event)
