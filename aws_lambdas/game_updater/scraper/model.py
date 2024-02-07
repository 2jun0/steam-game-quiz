from typing import Optional, Sequence

from pydantic import BaseModel, Field


class Game(BaseModel):
    steam_id: int
    name: str
    kr_name: Optional[str] = Field(default=None)
    released_at: float
    genres: Sequence[str]
    tags: Sequence[str]
    revenue: float