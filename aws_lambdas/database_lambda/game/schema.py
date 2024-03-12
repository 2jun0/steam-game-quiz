from collections.abc import Sequence
from typing import TypedDict

STEAM_ID = int


class SaveGame(TypedDict):
    steam_id: int
    name: str
    aliases: Sequence[str]
    released_at: float
    genres: Sequence[str]
