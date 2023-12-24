from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field


class UpdatedAtMixin(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CreatedAtMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
