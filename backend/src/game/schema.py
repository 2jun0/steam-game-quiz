from typing import Sequence

from pydantic import BaseModel


class AutoCompleteNameResponse(BaseModel):
    games: Sequence[str]
