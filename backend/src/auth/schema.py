from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    rank_score: int
