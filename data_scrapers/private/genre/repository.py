from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Genre


def get_genre(session: Session, *, name: str) -> Optional[Genre]:
    return session.scalars(select(Genre).where(Genre.name == name)).first()
