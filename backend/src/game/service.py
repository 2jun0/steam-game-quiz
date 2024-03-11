from elasticsearch import AsyncElasticsearch

from ..es import GAME_INDEX
from .schema import AutoCompleteName


class GameService:
    def __init__(self, es_client: AsyncElasticsearch) -> None:
        self._es_client = es_client

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
