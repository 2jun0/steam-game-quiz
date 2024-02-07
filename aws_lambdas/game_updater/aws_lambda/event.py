from typing import Any, Literal, TypedDict

EventName = Literal["save_games"]


class Event(TypedDict):
    name: EventName
    payload: Any
