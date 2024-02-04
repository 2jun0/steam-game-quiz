from typing import Any, Literal, TypedDict

EventName = Literal["get_all_games", "save_games", "save_screenshots"]


class Event(TypedDict):
    name: EventName
    payload: Any
