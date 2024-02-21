from elasticsearch import Elasticsearch
from sqlalchemy import select
from sqlalchemy.orm import Session

from database_lambda.game.model import Game
from database_lambda.game.schema import SaveGame
from database_lambda.game.service import get_all_games, save_games
from tests.database_lambda.utils.game import create_random_game
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
            "kr_name": "게임1",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure"],
        },
        {
            "steam_id": 2,
            "name": "game2",
            "kr_name": "게임2",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure", "RPG"],
        },
    ]
    save_games(games, session=session, es_client=es_client)

    saved = session.scalars(select(Game)).all()

    assert set(g["steam_id"] for g in games) == set(g.steam_id for g in saved)


def test_save_games은_이미_저장한_게임을_중복저장하지_않는다(session: Session, es_client: Elasticsearch):
    games: list[SaveGame] = [
        {
            "steam_id": 1,
            "name": "game1",
            "kr_name": "게임1",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure"],
        },
        {
            "steam_id": 2,
            "name": "game2",
            "kr_name": "게임2",
            "released_at": random_datetime().timestamp(),
            "genres": ["Adventure", "RPG"],
        },
    ]

    save_games(games, session=session, es_client=es_client)
    before_saved = session.scalars(select(Game)).all()

    save_games(games, session=session, es_client=es_client)
    after_saved = session.scalars(select(Game)).all()

    assert before_saved == after_saved


def test_save_games은_이미_저장한_게임은_업데이트_한다(session: Session, es_client: Elasticsearch):
    before_game: SaveGame = {
        "steam_id": 1,
        "name": "game1",
        "kr_name": "게임1",
        "released_at": random_datetime().timestamp(),
        "genres": ["Adventure"],
    }
    after_game: SaveGame = {
        "steam_id": 1,
        "name": "game2",
        "kr_name": "게임2",
        "released_at": random_datetime().timestamp(),
        "genres": ["Adventure", "RPG"],
    }

    save_games([before_game], session=session, es_client=es_client)
    save_games([after_game], session=session, es_client=es_client)
    saved = session.scalars(select(Game)).one().to_dto()

    assert saved.name == after_game["name"]
    assert saved.kr_name == after_game["kr_name"]
    assert saved.released_at.timestamp() == after_game["released_at"]
    assert saved.genres == after_game["genres"]
