from elasticsearch import AsyncElasticsearch

from .config import settings

GAME_INDEX = "game_index"

INDEXES = [GAME_INDEX]

es_client = AsyncElasticsearch(settings.ELASTIC_SEARCH_URL)
