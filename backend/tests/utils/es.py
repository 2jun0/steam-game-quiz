from meilisearch_python_sdk import AsyncClient

from src.es import INDEXES


async def delete_all_indexes(ms_client: AsyncClient):
    for index in INDEXES:
        try:
            task = await ms_client.delete_index(index)
            await ms_client.wait_for_task(task.task_uid)
        except Exception:
            pass


async def create_all_indexes(ms_client: AsyncClient):
    for index_name in INDEXES:
        try:
            await ms_client.create_index(index_name, primary_key="id")
        except Exception:
            pass
