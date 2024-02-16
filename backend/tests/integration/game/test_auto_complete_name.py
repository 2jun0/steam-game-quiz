import pytest
from elasticsearch import Elasticsearch
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.game.model import Game
from tests.utils.game import create_random_game, index_game


def create_indexed_game(session: Session, es_client: Elasticsearch, name: str) -> Game:
    game = create_random_game(session, name=name, kr_name="")
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
    assert res_json["games"] == [{"name": saved_game.name, "locale_name": None}]


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
