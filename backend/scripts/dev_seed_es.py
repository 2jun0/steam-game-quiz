import asyncio
import pathlib
import sys
from collections.abc import Generator, Iterable, Sequence
from typing import Any

from elasticsearch.helpers import async_bulk
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.database import engine  # noqa: E402
from src.es import GAME_INDEX, es_client  # noqa: E402
from src.game.model import Game  # noqa: E402


async def get_all_games(session: AsyncSession) -> Sequence[Game]:
    rs = await session.exec(select(Game))
    return rs.all()


def bulk_game_data(games: Iterable[Game]) -> Generator[dict[str, Any], Any, None]:
    for game in games:
        q_name = "".join([c if c.isalnum() else " " for c in game.name])
        yield {"_index": GAME_INDEX, "_id": game.id, "id": game.id, "name": game.name, "q_name": q_name}


async def main():
    try:
        await es_client.indices.delete(index=GAME_INDEX)
        await es_client.indices.create(index=GAME_INDEX)
    except Exception:
        pass

    async with AsyncSession(engine) as session:
        games = await get_all_games(session)

        # bulk index
        await async_bulk(es_client, bulk_game_data(games))

    await engine.dispose()

    await es_client.close()


asyncio.run(main())
