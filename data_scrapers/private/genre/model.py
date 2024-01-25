from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..model import Base, CreatedAtMixin, UpdatedAtMixin


class Genre(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    def to_dto(self) -> "GenreDto":
        return GenreDto(id=self.id, name=self.name)


class GenreDto(BaseModel):
    id: int
    name: str
