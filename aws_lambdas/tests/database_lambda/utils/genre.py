from typing import Optional

from sqlalchemy.orm import Session

from database_lambda.genre.model import Genre

genre_counter = 1


def create_random_genre(
    session: Session,
    *,
    name: Optional[str] = None,
) -> Genre:
    global genre_counter
    genre_counter += 1

    if name is None:
        name = f"Genre #{genre_counter}"

    genre = Genre(name=name)

    session.add(genre)
    session.commit()
    session.refresh(genre)

    return genre
