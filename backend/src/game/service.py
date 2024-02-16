from elasticsearch import AsyncElasticsearch

from ..es import GAME_INDEX
from .schema import AutoCompleteName


class GameService:
    def __init__(self, es_client: AsyncElasticsearch) -> None:
        self._es_client = es_client

    async def auto_complete_name(self, query: str) -> list[AutoCompleteName]:
        game_names = await self._search_game_name(query)

        return [AutoCompleteName(name=name, locale_name=None) for name in game_names]

    async def _search_game_name(self, query: str) -> list[str]:
        game_names: list[str] = []
        res = await self._es_client.search(
            index=GAME_INDEX,
            body={
                "query": {
                    "bool": {
                        "should": [
                            {"match_phrase_prefix": {"q_name": {"query": query.lower()}}},
                            {"match_phrase_prefix": {"name": {"query": query.lower()}}},
                        ]
                    }
                }
            },
        )

        for hit in res["hits"]["hits"]:
            name = hit["_source"]["name"]
            game_names.append(name)

        return game_names
