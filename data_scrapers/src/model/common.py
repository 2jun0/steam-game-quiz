from typing import Optional
from datetime import datetime
from sqlmodel import Field


class UpdatedAtMixin:
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)


class CreatedAtMixin:
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
