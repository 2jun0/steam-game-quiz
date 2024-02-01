import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.game.model import Game
from tests.utils.game import create_random_game


@pytest.fixture
def normal_game(session: Session) -> Game:
    # 평범한 게임: 게임의 이름의 길이는 3보다 커야 한다.
    game = create_random_game(session, name="NieR:Automata", kr_name="니어 오토마타")
    assert len(game.name) >= 3

    return game


@pytest.fixture
def short_name_game(session: Session) -> Game:
    # 짧은 길이의 게임: 게임의 이름의 길이는 3보다 커야 한다.
    game = create_random_game(session, name="Z", kr_name="Z")
    assert len(game.name) < 3

    return game


def test_auto_complete_game_name_with_too_long_query(client: TestClient, normal_game: Game):
    """게임 이름 보다 긴 쿼리의 경우, 아무것도 응답하지 않아야 합니다."""
    left = "ee" + normal_game.name
    right = normal_game.name + "ee"
    lr = "ee" + normal_game.name + "ee"

    for query in [left, right, lr]:
        res = client.get(f"/game/auto_complete_name?query={query}")
        assert res.status_code == status.HTTP_200_OK

        res_json = res.json()
        assert len(res_json["games"]) == 0


def test_auto_complete_game_name_for_short_query(client: TestClient, normal_game: Game):
    """쿼리가 3이하인 경우 (너무 짧은 경우), 아무것도 응답하지 않아야 합니다."""
    short_query = "a"

    res = client.get(f"/game/auto_complete_name?query={short_query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["games"]) == 0


def test_auto_complete_game_name(client: TestClient, normal_game: Game):
    # query total name
    total_name = normal_game.name

    # query partial name (right)
    r_partial_name = normal_game.name[-3:]

    # query partial name (left)
    l_partial_name = normal_game.name[:3]

    # query partial name (mid)
    mid = len(normal_game.name) // 2
    m_partial_name = normal_game.name[mid - 1 : mid + 2]

    for query in [total_name, r_partial_name, l_partial_name, m_partial_name]:
        res = client.get(f"/game/auto_complete_name?query={query}")
        assert res.status_code == status.HTTP_200_OK

        res_json = res.json()
        assert res_json["games"] == [{"name": normal_game.name, "locale_name": normal_game.kr_name}]


def test_auto_complete_short_game_name(client: TestClient, short_name_game: Game):
    # query total name
    total_name = short_name_game.name
    res = client.get(f"/game/auto_complete_name?query={total_name}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["games"] == [{"name": short_name_game.name, "locale_name": short_name_game.kr_name}]


def test_auto_complete_with_kr_game_name(client: TestClient, normal_game: Game):
    kr_name = normal_game.kr_name
    res = client.get(f"/game/auto_complete_name?query={kr_name}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["games"] == [{"name": normal_game.name, "locale_name": normal_game.kr_name}]


def test_auto_complete_for_multiple_games(client: TestClient, session: Session):
    create_random_game(session, name="game1", kr_name="ㅇㅇ")
    create_random_game(session, name="game2", kr_name="ㅇㅇ2")
    create_random_game(session, name="gggg", kr_name="game3")
    create_random_game(session, name="gggg", kr_name="game4")
    query = "game"

    res = client.get(f"/game/auto_complete_name?query={query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["games"]) == 4
