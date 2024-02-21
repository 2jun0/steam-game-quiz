from elasticsearch import Elasticsearch

from database_lambda.config import setting
from database_lambda.es import INDEXES

es_client = Elasticsearch(setting.ELASTIC_SEARCH_URL)


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
