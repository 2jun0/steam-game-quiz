from elasticsearch import Elasticsearch

from .config import setting

GAME_INDEX = "game_index"

INDEXES = [GAME_INDEX]

es_client = Elasticsearch(setting.ELASTIC_SEARCH_URL)
