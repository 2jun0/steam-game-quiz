import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine

from tests.config import TestConfig


@pytest.fixture(autouse=True)
def mock_config(mocker: MockerFixture):
    mocker.patch("src.config.Config", TestConfig)


def test_scrap_games_job(engine: Engine):
    from src.lambda_function import scrap_games_job

    scrap_games_job(engine)


def test_scrap_screenshots_job(engine: Engine):
    from src.lambda_function import scrap_games_job, scrap_screenshots_job

    scrap_games_job(engine)

    scrap_screenshots_job(engine)
