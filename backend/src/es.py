from meilisearch_python_sdk import AsyncClient

from .config import settings

GAME_INDEX = "game_index"

INDEXES = [GAME_INDEX]

ms_client = AsyncClient(settings.MEILISEARCH_URL, settings.MEILISEARCH_MASTER_KEY)
