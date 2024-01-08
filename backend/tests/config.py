from pydantic import MySQLDsn
from pydantic_settings import BaseSettings


class TestConfig(BaseSettings):
    TEST_DATABASE_URL: MySQLDsn | str


test_settings = TestConfig()  # type: ignore
