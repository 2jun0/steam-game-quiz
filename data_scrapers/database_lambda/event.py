from typing import Any, Literal, TypedDict

EventName = Literal[
    "save_games",
    "save_screenshots",
    "get_games_in_steam_ids",
    "get_some_games",
    "get_screenshots_in_steam_file_ids",
]


class Event(TypedDict):
    name: EventName
    payload: Any
