from datetime import datetime
from random import randint


def random_datetime() -> datetime:
    return datetime(year=randint(1999, 2024), month=randint(1, 12), day=randint(1, 20))
