from sqlmodel import Field, SQLModel

from ..model import CreatedAtMixin, UpdatedAtMixin


class Guest(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
