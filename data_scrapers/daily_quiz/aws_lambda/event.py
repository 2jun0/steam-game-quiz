from typing import Any, Literal, TypedDict

EventName = Literal["save_screenshots", "save_quizzes", "get_all_games"]


class Event(TypedDict):
    name: EventName
    payload: Any
