import pytest
from pytest_mock import MockerFixture

from tests.config import TestConfig


@pytest.fixture(autouse=True)
def mock_config(mocker: MockerFixture):
    mocker.patch("src.config.Config", TestConfig)


def test_scrap_games_job():
    from src.main import scrap_games_job

    scrap_games_job()


def test_scrap_screenshots_job():
    from src.main import scrap_games_job, scrap_screenshots_job

    scrap_games_job()

    scrap_screenshots_job()
