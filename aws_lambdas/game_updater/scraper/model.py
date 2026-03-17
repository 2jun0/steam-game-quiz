from typing import Sequence

from pydantic import BaseModel


class Game(BaseModel):
    steam_id: int
    name: str
    released_at: float
    genres: Sequence[str]
    copies_sold: int
