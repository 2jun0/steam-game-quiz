from faker import Faker

faker = Faker(["ko-KR", "ja-JP", "en-US"])


def random_name() -> str:
    return faker.name()


def random_kr_string() -> str:
    return faker["ko-KR"].name()  # type: ignore


def random_image_url() -> str:
    return faker.image_url()
