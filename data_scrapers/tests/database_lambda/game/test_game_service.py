from sqlalchemy import select
from sqlalchemy.orm import Session

from database_lambda.game.model import Game
from database_lambda.game.service import get_games_in_steam_ids, get_some_games, save_games
from tests.database_lambda.utils.game import create_random_game
from tests.database_lambda.utils.utils import random_datetime


def test_get_some_games은_게임을_가져와야한다(session: Session):
    _ = [create_random_game(session) for _ in range(2)]

    given = get_some_games(session)
    assert len(given) == 2


def test_save_games은_입력한_게임을_저장해야_한다(session: Session):
    games = [
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
    save_games(session, games)

    saved = session.scalars(select(Game)).all()

    assert set(g["steam_id"] for g in games) == set(g.steam_id for g in saved)


def test_save_games은_이미_저장한_게임을_중복저장하지_않는다(session: Session):
    games = [
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

    save_games(session, games)
    before_saved = session.scalars(select(Game)).all()

    save_games(session, games)
    after_saved = session.scalars(select(Game)).all()

    assert before_saved == after_saved


def test_save_games은_이미_저장한_게임은_업데이트_한다(session: Session):
    before_game = {
        "steam_id": 1,
        "name": "game1",
        "kr_name": "게임1",
        "released_at": random_datetime().timestamp(),
        "genres": ["Adventure"],
    }
    after_game = {
        "steam_id": 1,
        "name": "game2",
        "kr_name": "게임2",
        "released_at": random_datetime().timestamp(),
        "genres": ["Adventure", "RPG"],
    }

    save_games(session, [before_game])
    save_games(session, [after_game])
    saved = session.scalars(select(Game)).one().to_dto()

    assert saved.name == after_game["name"]
    assert saved.kr_name == after_game["kr_name"]
    assert saved.released_at.timestamp() == after_game["released_at"]
    assert saved.genres == after_game["genres"]


def test_get_games_in_steam_ids은_입력한_스팀_id에_맞는_게임을_가져와야한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]

    steam_ids = [saved_games[0].steam_id, saved_games[1].steam_id]
    games = get_games_in_steam_ids(session, steam_ids)

    assert set(g["id"] for g in games) == set((saved_games[0].id, saved_games[1].id))
