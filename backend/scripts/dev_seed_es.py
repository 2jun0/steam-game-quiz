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
from src.es import es_client  # noqa: E402
from src.game.model import Game  # noqa: E402

GAME_INDEX = "game_index"


async def get_all_games(session: AsyncSession) -> Sequence[Game]:
    rs = await session.exec(select(Game))
    return rs.all()


def bulk_game_data(games: Iterable[Game]) -> Generator[dict[str, Any], Any, None]:
    for game in games:
        yield {"_index": GAME_INDEX, "id": game.id, "name": game.name}


async def main():
    await es_client.indices.create(index=GAME_INDEX)

    async with AsyncSession(engine) as session:
        games = await get_all_games(session)

        # bulk index
        await async_bulk(es_client, bulk_game_data(games))

    await engine.dispose()

    await es_client.close()


asyncio.run(main())
