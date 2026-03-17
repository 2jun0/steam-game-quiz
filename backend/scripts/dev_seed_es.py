import asyncio
import pathlib
import sys
from collections.abc import Iterable
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.database import engine  # noqa: E402
from src.es import GAME_INDEX, ms_client  # noqa: E402
from src.game.model import Game  # noqa: E402


async def get_all_games(session: AsyncSession):
    rs = await session.exec(select(Game))
    return rs.all()


def game_docs(games: Iterable[Game]) -> list[dict[str, Any]]:
    docs = []
    for game in games:
        q_name = "".join([c if c.isalnum() else " " for c in game.name])
        docs.append({
            "id": game.id,
            "name": game.name,
            "q_name": q_name,
            "aliases": [alias.name for alias in game.aliases],
        })
    return docs


async def main():
    try:
        task = await ms_client.delete_index(GAME_INDEX)
        await ms_client.wait_for_task(task.task_uid)
    except Exception:
        pass

    await ms_client.create_index(GAME_INDEX, primary_key="id")

    async with AsyncSession(engine) as session:
        games = await get_all_games(session)
        index = ms_client.index(GAME_INDEX)
        task = await index.add_documents(game_docs(games))
        await ms_client.wait_for_task(task.task_uid)

    await engine.dispose()
    await ms_client.aclose()


asyncio.run(main())
