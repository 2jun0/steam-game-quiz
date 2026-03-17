from meilisearch_python_sdk import AsyncClient

from ..es import GAME_INDEX
from .repository import SolvedGameRepository
from .schema import AutoCompleteName


class GameService:
    def __init__(self, *, ms_client: AsyncClient, solved_game_repository: SolvedGameRepository) -> None:
        self._ms_client = ms_client

    async def auto_complete_name(self, query: str) -> list[AutoCompleteName]:
        auto_complete_names: list[AutoCompleteName] = []
        result = await self._ms_client.index(GAME_INDEX).search(
            query,
            attributes_to_search_on=["q_name", "name", "aliases"],
            show_matches_position=True,
        )

        for hit in result.hits:
            name: str = hit["name"]
            matches: dict = hit.get("_matchesPosition", {})

            if "q_name" in matches or "name" in matches:
                match = name
            elif "aliases" in matches:
                alias_idx = matches["aliases"][0].get("attributeIndex", 0)
                match = hit["aliases"][alias_idx]
            else:
                match = name

            auto_complete_names.append(AutoCompleteName(name=name, match=match))

        return auto_complete_names
