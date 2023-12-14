from collections import OrderedDict
from datetime import datetime
from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def to_json(self) -> OrderedDict[str, Any]:
        result: OrderedDict[str, Any] = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
