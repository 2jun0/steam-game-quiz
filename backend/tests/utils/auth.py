from sqlmodel import Session

from src.auth.model import User

QUIZ_SCREENSHOT_COUNT = 5


def create_random_user(
    session: Session, *, email: str, is_active: bool = True, is_superuser: bool = False, is_verified: bool = False
) -> User:
    user = User(
        email=email,
        hashed_password="hashed_password",
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user