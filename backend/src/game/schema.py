from typing import Sequence

from pydantic import BaseModel


class AutoCompleteName(BaseModel):
    name: str
    match: str


class AutoCompleteNameResponse(BaseModel):
    games: Sequence[AutoCompleteName]
