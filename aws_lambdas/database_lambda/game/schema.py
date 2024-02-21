from collections.abc import Sequence
from typing import Optional, TypedDict

STEAM_ID = int


class SaveGame(TypedDict):
    steam_id: int
    name: str
    kr_name: Optional[str]
    released_at: float
    genres: Sequence[str]
