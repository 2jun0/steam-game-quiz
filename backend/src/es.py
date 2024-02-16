from elasticsearch import AsyncElasticsearch

from .config import settings

es_client = AsyncElasticsearch(settings.ELASTIC_SEARCH_URL)
