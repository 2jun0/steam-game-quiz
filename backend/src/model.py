from datetime import datetime

from sqlmodel import Field


class UpdatedAtMixin:
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CreatedAtMixin:
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
