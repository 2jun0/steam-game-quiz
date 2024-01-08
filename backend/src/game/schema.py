from typing import Sequence

from pydantic import BaseModel


class AutoCompleteName(BaseModel):
    name: str
    locale_name: str | None


class AutoCompleteNameResponse(BaseModel):
    games: Sequence[AutoCompleteName]
