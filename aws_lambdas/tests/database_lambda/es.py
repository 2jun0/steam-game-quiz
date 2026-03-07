import meilisearch

from database_lambda.config import setting
from database_lambda.es import INDEXES

ms_client = meilisearch.Client(setting.MEILISEARCH_URL)


def delete_all_indexes(client: meilisearch.Client):
    for index in INDEXES:
        try:
            task = client.delete_index(index)
            client.wait_for_task(task.task_uid)
        except Exception:
            pass


def create_all_indexes(client: meilisearch.Client):
    for index_name in INDEXES:
        try:
            client.create_index(index_name, {"primaryKey": "id"})
        except Exception:
            pass
