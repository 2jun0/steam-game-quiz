from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow, nullable=False)


class CreatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow, nullable=False)
