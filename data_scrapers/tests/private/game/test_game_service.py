from sqlalchemy import select
from sqlalchemy.orm import Session

from private.game.model import Game
from private.game.service import get_games_in_steam_ids, get_some_games, save_games
from tests.private.utils.game import create_random_game
from tests.private.utils.utils import random_datetime


def test_get_some_games은_게임을_가져와야한다(session: Session):
    _ = [create_random_game(session) for _ in range(2)]

    given = get_some_games(session)
    assert len(given) == 2


def test_save_games은_입력한_게임을_저장해야_한다(session: Session):
    random_datetime().timestamp

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


def test_get_games_in_steam_ids은_입력한_스팀_id에_맞는_게임을_가져와야한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]

    steam_ids = [saved_games[0].steam_id, saved_games[1].steam_id]
    games = get_games_in_steam_ids(session, steam_ids)

    assert set(g["id"] for g in games) == set((saved_games[0].id, saved_games[1].id))
