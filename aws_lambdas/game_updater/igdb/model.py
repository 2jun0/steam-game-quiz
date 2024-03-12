from typing import TypedDict


class IGDBExternalGames(TypedDict):
    id: int
    uid: str
    game: int


class IGDBGame(TypedDict):
    id: int
    alternative_names: list[int]


class IGDBAlternativeName(TypedDict):
    id: int
    name: str
    game: int
