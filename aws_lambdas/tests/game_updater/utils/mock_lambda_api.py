from datetime import datetime
from typing import Sequence

from game_updater.aws_lambda.model import Game, SaveGame
from game_updater.protocols import LambdaAPI


class MockLambdaAPI(LambdaAPI):
    def __init__(self):
        self.games: dict[int, Game] = {}

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
