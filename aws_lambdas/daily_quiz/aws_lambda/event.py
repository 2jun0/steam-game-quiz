from typing import Any, Literal, TypedDict

EventName = Literal["save_screenshots", "save_quizzes", "get_all_games", "save_daily_quizzes"]


class Event(TypedDict):
    name: EventName
    payload: Any
