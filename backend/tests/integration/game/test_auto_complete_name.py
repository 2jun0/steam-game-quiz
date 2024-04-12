import pytest
from elasticsearch import AsyncElasticsearch
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.game.model import Game
from tests.utils.game import create_random_game, index_game


async def create_indexed_game(
    session: AsyncSession, es_client: AsyncElasticsearch, name: str, aliases: list[str] = []
) -> Game:
    game = await create_random_game(session, name=name, aliases=aliases)
    await index_game(es_client, game)
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
async def test_auto_complete_game_name(
    client: AsyncClient, session: AsyncSession, es_client: AsyncElasticsearch, game_name: str, query: str
):
    saved_game = await create_indexed_game(session, es_client, game_name)

    res = await client.get(f"/game/auto_complete_name?query={query}")
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
async def test_auto_complete_game_name_by_alias(
    client: AsyncClient, session: AsyncSession, es_client: AsyncElasticsearch, game_name: str, alias: str, query: str
):
    saved_game = await create_indexed_game(session, es_client, game_name, [alias])

    res = await client.get(f"/game/auto_complete_name?query={query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert res_json["games"] == [{"name": saved_game.name, "match": alias}]


async def test_auto_complete_for_multiple_games(
    client: AsyncClient, session: AsyncSession, es_client: AsyncElasticsearch
):
    await create_indexed_game(session, es_client, name="game1")
    await create_indexed_game(session, es_client, name="game2")
    await create_indexed_game(session, es_client, name="game3")
    await create_indexed_game(session, es_client, name="game4")
    query = "game"

    res = await client.get(f"/game/auto_complete_name?query={query}")
    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()
    assert len(res_json["games"]) == 4
