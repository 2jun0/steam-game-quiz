"""
개발 환경에서 테스트할때 사용할 시드 데이터를 만듭니다.
이 코드는 유지보수되지 않거나 버려질 수 있습니다.
"""
import asyncio
import pathlib
import sys
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.database import engine
from src.game.model import Game, GameScreenshot
from src.quiz.model import Quiz


async def seed_game(session: AsyncSession) -> Game:
    game = Game(name="NieR:Automata™", kr_name="NieR:Automata™", steam_id=524220)
    session.add(game)
    await session.commit()
    await session.refresh(game)

    return game


async def seed_screenshots(session: AsyncSession, *, game_id: int) -> list[GameScreenshot]:
    screenshots = [
        GameScreenshot(
            steam_file_id=1,
            url="https://steamuserimages-a.akamaihd.net/ugc/2274945577051010624/117A19A3AA4F37B31808F949D93ADFECA2E2A909/",
            game_id=game_id,
        ),
        GameScreenshot(
            steam_file_id=2,
            url="https://steamuserimages-a.akamaihd.net/ugc/2274945577051012062/1FED87C640612B4AE83FFA418E0A0A6C1090200F/",
            game_id=game_id,
        ),
        GameScreenshot(
            steam_file_id=3,
            url="https://steamuserimages-a.akamaihd.net/ugc/2267065063333057855/F93A4BE574428818E7EE8E030B195E1038DBEBF6/",
            game_id=game_id,
        ),
        GameScreenshot(
            steam_file_id=4,
            url="https://steamuserimages-a.akamaihd.net/ugc/2267065063325393453/747F164746997CE33616B47A1EF2471FC372449D/",
            game_id=game_id,
        ),
        GameScreenshot(
            steam_file_id=5,
            url="https://steamuserimages-a.akamaihd.net/ugc/2274945577051011680/580F9DA393364FD0DBB48096BF1652E21558BA13/",
            game_id=game_id,
        ),
    ]
    session.add_all(screenshots)

    await session.commit()
    for s in screenshots:
        await session.refresh(s)

    return screenshots


async def seed_quiz(session: AsyncSession, *, screenshots: Sequence[GameScreenshot]) -> Quiz:
    quiz = Quiz()
    for s in screenshots:
        quiz.screenshots.append(s)
    session.add(quiz)

    await session.commit()
    await session.refresh(quiz)

    return quiz


async def seed_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        game = await seed_game(session)
        assert game.id is not None
        screenshots = await seed_screenshots(session, game_id=game.id)
        await seed_quiz(session, screenshots=screenshots)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_db())
