from elasticsearch import AsyncElasticsearch

from src.es import INDEXES


async def delete_all_indexes(es_client: AsyncElasticsearch):
    for index in INDEXES:
        try:
            await es_client.indices.delete(index=index)
        except Exception:
            pass


async def create_all_indexes(es_client: AsyncElasticsearch):
    for index in INDEXES:
        try:
            await es_client.indices.create(index=index)
        except Exception:
            pass
