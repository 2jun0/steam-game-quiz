from collections.abc import Sequence
from datetime import date
from typing import TypedDict

from ..screenshot.schema import SaveGameScreenshot


class SaveQuiz(TypedDict):
    screenshots: Sequence[SaveGameScreenshot]


class SaveDailyQuiz(TypedDict):
    quiz: SaveQuiz
    target_date: date
