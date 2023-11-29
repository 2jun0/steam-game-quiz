from typing import Optional
from sqlmodel import Field, SQLModel
from ..model import CreatedAtMixin, UpdatedAtMixin


class Game(SQLModel, CreatedAtMixin, UpdatedAtMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    steam_id: int = Field(unique=True)
    name: str = Field(max_length=64, nullable=False)
    kr_name: str = Field(max_length=64)


class GameScreenshot(SQLModel, CreatedAtMixin, UpdatedAtMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # TODO: FK를 넣지 않을거야! 하지만 lazy key? 같은 옵션이 있는지 찾아봐
    game_id: Optional[int] = Field(nullable=False)
    url: str = Field(max_length=2048, nullable=False)
    provider: str = Field(max_length=256)
