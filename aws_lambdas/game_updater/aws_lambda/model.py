from typing import Sequence

from pydantic import BaseModel


class SaveGame(BaseModel):
    steam_id: int
    name: str
    released_at: float
    genres: Sequence[str]
    aliases: Sequence[str]
