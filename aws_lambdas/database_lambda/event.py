from typing import Any, Literal, TypedDict

EventName = Literal["get_all_games", "save_games", "save_screenshots", "save_quizzes", "save_daily_quizzes"]


class Event(TypedDict):
    name: EventName
    payload: Any
