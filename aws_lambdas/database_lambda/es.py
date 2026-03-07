import meilisearch

from .config import setting

GAME_INDEX = "game_index"

INDEXES = [GAME_INDEX]

ms_client = meilisearch.Client(setting.MEILISEARCH_URL)
