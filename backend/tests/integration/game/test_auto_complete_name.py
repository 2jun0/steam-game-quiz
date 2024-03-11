from collections.abc import Generator
from typing import Any

import pytest
from elasticsearch import Elasticsearch
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.game.model import Game
from src.main import app
from tests.utils.game import create_random_game, index_game


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


def create_indexed_game(session: Session, es_client: Elasticsearch, name: str, aliases: list[str] = []) -> Game:
    game = create_random_game(session, name=name, aliases=aliases)
    index_game(es_client, game)
    return game


@pytest.mark.parametrize(
    ("game_name", "query"),
    (
        ("NieR:Automata", "nier"),
        ("NieR:Automata", "ni"),
        ("NieR:Automata", "Ni"),
        ("NieR:Automata", "Nier"),
        ("NieR:Automata", "Automata"),
        ("NieR:Automata", "Au"),
        ("NieR:Automata", "auto"),
        ("Nier:Automata", "nier:auto"),
    ),
)
def test_auto_complete_game_name(
    client: TestClient, session: Session, es_client: Elasticsearch, game_name: str, query: str
):
    saved_game = create_indexed_game(session, es_client, game_name)

    res = client.get(f"/game/auto_complete_name?query={query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["games"] == [{"name": saved_game.name, "match": saved_game.name}]


@pytest.mark.parametrize(
    ("game_name", "alias", "query"),
    (
        ("NieR:Automata", "니어오토마타", "니어"),
        ("NieR:Automata", "니어오토마타", "니어오토마타"),
        ("NieR:Automata", "오토마타", "오토"),
    ),
)
def test_auto_complete_game_name_by_alias(
    client: TestClient, session: Session, es_client: Elasticsearch, game_name: str, alias: str, query: str
):
    saved_game = create_indexed_game(session, es_client, game_name, [alias])

    res = client.get(f"/game/auto_complete_name?query={query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["games"] == [{"name": saved_game.name, "match": alias}]


def test_auto_complete_for_multiple_games(client: TestClient, session: Session, es_client: Elasticsearch):
    create_indexed_game(session, es_client, name="game1")
    create_indexed_game(session, es_client, name="game2")
    create_indexed_game(session, es_client, name="game3")
    create_indexed_game(session, es_client, name="game4")
    query = "game"

    res = client.get(f"/game/auto_complete_name?query={query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["games"]) == 4
