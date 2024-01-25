from datetime import datetime
from typing import Sequence

from public.aws_lambda.model import Game, GameScreenshot, SaveGame
from public.protocols import LambdaAPI


class MockLambdaAPI(LambdaAPI):
    def __init__(self):
        self.games: dict[int, Game] = {}
        self.screenshots: dict[int, GameScreenshot] = {}

    def get_some_games(self) -> list[Game]:
        return list(self.games.values())

    def get_games_in_steam_ids(self, steam_ids: Sequence[int]) -> list[Game]:
        return [self.games[id] for id in steam_ids if id in self.games]

    def get_screenshots_in_steam_file_ids(self, steam_file_ids: Sequence[int]) -> list[GameScreenshot]:
        return [self.screenshots[id] for id in steam_file_ids if id in self.screenshots]

    def save_games(self, games: Sequence[SaveGame]):
        for game in games:
            self.games[game.steam_id] = Game(
                id=game.steam_id,
                steam_id=game.steam_id,
                name=game.name,
                kr_name=game.kr_name,
                released_at=datetime.fromtimestamp(game.released_at),
                genres=game.genres,
                updated_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
            )

    def save_screenshots(self, screenshots: Sequence[GameScreenshot]):
        for screenshot in screenshots:
            self.screenshots[screenshot.steam_file_id] = screenshot
