from datetime import date, datetime
from random import randint

import dateutil.parser
from faker import Faker

faker = Faker(["ko-KR", "ja-JP", "en-US"])


def random_name() -> str:
    return faker.name()


def random_kr_string() -> str:
    return faker["ko-KR"].name()  # type: ignore


def random_image_url() -> str:
    return faker.image_url()


def random_email() -> str:
    return faker["en-US"].name().replace(" ", "_") + "@exam.com"  # type: ignore


def random_bool() -> bool:
    return randint(0, 1) == 1


def jsontime2datetime(jsontime: str) -> datetime:
    return dateutil.parser.parse(jsontime)
