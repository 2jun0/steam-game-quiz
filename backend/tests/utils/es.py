from elasticsearch import Elasticsearch

from src.es import INDEXES


def delete_all_indexes(es_client: Elasticsearch):
    for index in INDEXES:
        try:
            es_client.indices.delete(index=index)
        except Exception:
            pass


def create_all_indexes(es_client: Elasticsearch):
    for index in INDEXES:
        try:
            es_client.indices.create(index=index)
        except Exception:
            pass
