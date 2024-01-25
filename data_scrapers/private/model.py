from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
