import pytest
from elasticsearch import Elasticsearch
from sqlalchemy import select
from sqlalchemy.orm import Session

from database_lambda.game.model import Game
from database_lambda.game.schema import SaveGame
from database_lambda.game.service import get_all_games, save_games
from tests.database_lambda.utils.game import create_random_game, search_game_docs
from tests.database_lambda.utils.utils import random_datetime


def test_get_all_games은_게임을_가져와야한다(session: Session):
    saved = [create_random_game(session) for _ in range(2)]

    given = get_all_games(session=session)
    assert set(g["id"] for g in given) == set(g.id for g in saved)


def test_save_games은_입력한_게임을_저장해야_한다(session: Session, es_client: Elasticsearch):
    games: list[SaveGame] = [
        {
            "steam_id": 1,
            "name": "game1",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure"],
            "aliases": ["게임1", "game 1"],
        },
        {
            "steam_id": 2,
            "name": "game2",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure", "RPG"],
            "aliases": ["게임2", "game 2"],
        },
    ]
    save_games(games, session=session, es_client=es_client)

    # check rdb
    models = session.scalars(select(Game)).all()
    assert set(g["steam_id"] for g in games) == set(g.steam_id for g in models)

    # check es
    docs = search_game_docs(es_client)
    assert set(g["name"] for g in games) == set(g["_source"]["name"] for g in docs)
    assert set(g.id for g in models) == set(g["_source"]["id"] for g in docs)


def test_save_games은_이미_저장한_게임을_중복저장하지_않는다(session: Session, es_client: Elasticsearch):
    games: list[SaveGame] = [
        {
            "steam_id": 1,
            "name": "game1",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure"],
            "aliases": ["게임1", "game 1"],
        },
        {
            "steam_id": 2,
            "name": "game2",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure", "RPG"],
            "aliases": ["게임2", "game 2"],
        },
    ]

    save_games(games, session=session, es_client=es_client)
    before_saved = session.scalars(select(Game)).all()
    before_docs = search_game_docs(es_client)

    save_games(games, session=session, es_client=es_client)
    after_saved = session.scalars(select(Game)).all()
    after_docs = search_game_docs(es_client)

    assert before_saved == after_saved
    assert before_docs == after_docs


@pytest.mark.parametrize(
    ("before_game", "after_game"),
    (
        (
            {
                "steam_id": 1,
                "name": "game1",
                "released_at": random_datetime().timestamp(),
                "genres": ["Adventure"],
                "aliases": ["게임", "게임1", "game 1"],
            },
            {
                "steam_id": 1,
                "name": "game2",
                "released_at": random_datetime().timestamp(),
                "genres": ["RPG", "Adventure"],
                "aliases": ["게임", "게임2", "game 2"],
            },
        ),
        (
            {
                "steam_id": 1,
                "name": "game2",
                "released_at": random_datetime().timestamp(),
                "genres": ["Adventure", "RPG"],
                "aliases": ["게임", "게임2", "game 2"],
            },
            {
                "steam_id": 1,
                "name": "game1",
                "released_at": random_datetime().timestamp(),
                "genres": ["Adventure"],
                "aliases": ["게임", "게임1", "game 1"],
            },
        ),
    ),
)
def test_save_games은_이미_저장한_게임은_업데이트_한다(
    session: Session, es_client: Elasticsearch, before_game: SaveGame, after_game: SaveGame
):
    save_games([before_game], session=session, es_client=es_client)
    save_games([after_game], session=session, es_client=es_client)

    # check rdb
    saved = session.scalars(select(Game)).one().to_dto()
    assert saved.name == after_game["name"]
    assert set(saved.aliases) == set(after_game["aliases"])
    assert set(saved.genres) == set(after_game["genres"])

    # check es
    docs = search_game_docs(es_client)
    assert len(docs) == 1
    assert docs[0]["_source"]["name"] == after_game["name"]


def test_save_games은_별칭을_저장한다(session: Session, es_client: Elasticsearch):
    game: SaveGame = {
        "steam_id": 1,
        "name": "game1",
        "released_at": random_datetime().timestamp(),
        "genres": ["Adventure"],
        "aliases": ["게임1", "game 1"],
    }

    save_games([game], session=session, es_client=es_client)

    # check es
    docs = search_game_docs(es_client)
    game_doc = docs[0]["_source"]

    assert set(game["aliases"]) == set(game_doc["aliases"])
