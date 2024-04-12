from .model import SolvedGame
from .repository import SolvedGameRepository


class GameManager:
    def __init__(self, *, solved_game_repository: SolvedGameRepository) -> None:
        self._solved_game_repo = solved_game_repository

    async def solve_game(self, *, game_id: int, user_id: int):
        exists = await self.has_solved_game(game_id=game_id, user_id=user_id)
        if not exists:
            solved_game = SolvedGame(user_id=user_id, game_id=game_id)
            await self._solved_game_repo.create(model=solved_game)

    async def has_solved_game(self, *, game_id: int, user_id: int):
        return await self._solved_game_repo.exists_by_user_and_game(user_id=user_id, game_id=game_id)
