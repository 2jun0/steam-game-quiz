from faker import Faker

faker = Faker()


def random_name() -> str:
    return faker.name()


def random_kr_string() -> str:
    return faker["ko-KR"].name()


def random_image_url() -> str:
    return faker.image_url()
