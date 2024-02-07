from collections.abc import Sequence
from typing import TypedDict

from ..screenshot.schema import SaveGameScreenshot


class SaveQuiz(TypedDict):
    screenshots: Sequence[SaveGameScreenshot]
