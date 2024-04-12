from asyncio import Lock
from datetime import datetime

from elasticsearch import AsyncElasticsearch
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.es import GAME_INDEX
from src.game.model import Game, GameAlias, SolvedGame

from .utils import random_datetime, random_name

steam_id_counter = 0
steam_id_lock = Lock()


async def create_random_game(
    session: AsyncSession, *, name: str | None = None, released_at: datetime | None = None, aliases: list[str] = []
) -> Game:
    global steam_id_counter

    if name is None:
        name = random_name()
    if released_at is None:
        released_at = random_datetime()

    async with steam_id_lock:
        steam_id_counter += 1
        game = Game(
            steam_id=steam_id_counter,
            name=name,
            released_at=released_at,
            aliases=[GameAlias(name=alias_name) for alias_name in aliases],
        )

    session.add(game)
    await session.commit()

    return game


async def get_solved_game(session: AsyncSession, *, user_id: int, game_id: int) -> SolvedGame | None:
    stmt = select(SolvedGame).where(SolvedGame.user_id == user_id, SolvedGame.game_id == game_id)
    rs = await session.exec(stmt)
    return rs.one_or_none()


async def index_game(es_client: AsyncElasticsearch, game: Game):
    q_name = "".join([c if c.isalnum() else " " for c in game.name])
    await es_client.index(
        index=GAME_INDEX,
        body={"q_name": q_name, "name": game.name, "aliases": [alias.name for alias in game.aliases], "id": game.id},
        refresh=True,
    )
