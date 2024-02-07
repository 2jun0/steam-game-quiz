from typing import TypedDict

STEAM_FILE_ID = int


class SaveGameScreenshot(TypedDict):
    steam_file_id: STEAM_FILE_ID
    url: str
    game_id: int
