from elasticsearch import AsyncElasticsearch

from ..es import GAME_INDEX
from .model import SolvedGame
from .repository import SolvedGameRepository
from .schema import AutoCompleteName


class GameService:
    def __init__(self, *, es_client: AsyncElasticsearch, solved_game_repository: SolvedGameRepository) -> None:
        self._es_client = es_client
        self._solved_game_repo = solved_game_repository

    async def auto_complete_name(self, query: str) -> list[AutoCompleteName]:
        auto_complete_names: list[AutoCompleteName] = []
        res = await self._es_client.search(
            index=GAME_INDEX,
            body={
                "query": {
                    "bool": {
                        "should": [
                            {"match_phrase_prefix": {"q_name": {"query": query.lower()}}},
                            {"match_phrase_prefix": {"name": {"query": query.lower()}}},
                            {"match_phrase_prefix": {"aliases": {"query": query.lower()}}},
                        ]
                    }
                },
                "highlight": {
                    "pre_tags": [""],
                    "post_tags": [""],
                    "fields": {"q_name": {}, "name": {}, "aliases": {}},
                },
            },
        )

        for hit in res["hits"]["hits"]:
            name: str = hit["_source"]["name"]

            highlight = hit["highlight"]
            if "q_name" in highlight or "name" in highlight:
                match = name
            elif "aliases" in highlight:
                match = highlight["aliases"][0]

            auto_complete_names.append(AutoCompleteName(name=name, match=match))

        return auto_complete_names

    async def on_correct_answer(self, *, game_id: int, user_id: int):
        exists = await self._solved_game_repo.exists_by_user_and_game(user_id=user_id, game_id=game_id)
        if not exists:
            await self._solve_game(user_id=user_id, game_id=game_id)

    async def _solve_game(self, *, user_id: int, game_id: int):
        solved_game = SolvedGame(user_id=user_id, game_id=game_id)
        await self._solved_game_repo.create(model=solved_game)

    # async def _validate_not_solved(self, *, user_id: int, game_id: int):
    #     solved = await self._solved_game_repo.exists_by_user_and_game(user_id=user_id, game_id=game_id)
    #     if solved:
    #         raise GameAlreadySolvedError
