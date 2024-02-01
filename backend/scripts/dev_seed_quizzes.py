"""
개발 환경에서 테스트할때 사용할 시드 데이터를 만듭니다.
이 코드는 유지보수되지 않거나 버려질 수 있습니다.
"""
import asyncio
import pathlib
import sys
from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.database import engine  # noqa: E402
from src.game.model import Game, GameScreenshot  # noqa: E402
from src.quiz.model import Quiz  # noqa: E402

screenshot_urls = {
    524220: [
        "https://steamuserimages-a.akamaihd.net/ugc/2274945577051010624/117A19A3AA4F37B31808F949D93ADFECA2E2A909/",
        "https://steamuserimages-a.akamaihd.net/ugc/2274945577051012062/1FED87C640612B4AE83FFA418E0A0A6C1090200F/",
        "https://steamuserimages-a.akamaihd.net/ugc/2267065063333057855/F93A4BE574428818E7EE8E030B195E1038DBEBF6/",
        "https://steamuserimages-a.akamaihd.net/ugc/2267065063325393453/747F164746997CE33616B47A1EF2471FC372449D/",
        "https://steamuserimages-a.akamaihd.net/ugc/2274945577051011680/580F9DA393364FD0DBB48096BF1652E21558BA13/",
    ],
    264710: [
        "https://steamuserimages-a.akamaihd.net/ugc/2303096012449082218/8C6CBE07F275EEE56E2EF75E1A95FE1CF2A19612/",
        "https://steamuserimages-a.akamaihd.net/ugc/2277199680699609330/CD40BC3B8D254C8CB7D7D577D23A548A7F15F390/",
        "https://steamuserimages-a.akamaihd.net/ugc/2303096012449072271/34F538C495EF0C68154165781BD1C205AE99E2C3/",
        "https://steamuserimages-a.akamaihd.net/ugc/2290711113456410885/B0C92E0033C05A3DCE776EE37890B512A67F2684/",
        "https://steamuserimages-a.akamaihd.net/ugc/2310976677862722087/051CCDDE076FCE4E9606DBF7E4E7A038DBEEA017/",
    ],
    427520: [
        "https://steamuserimages-a.akamaihd.net/ugc/2298592412798086605/5E5B8E95AA762C932242B5B2C80C5BC6654D8CEB/",
        "https://steamuserimages-a.akamaihd.net/ugc/2283956013868435178/9A8075E37DC3E1726F2A97FF9C15B623C954F67F/",
        "https://steamuserimages-a.akamaihd.net/ugc/2309851411898905888/AD5ECCFF05DD4B408128032B1D3A0B551AE8757D/",
        "https://steamuserimages-a.akamaihd.net/ugc/2305347812246726611/81F163FCBFCA9ADBC8C57C59DF41441D5347F42C/",
        "https://steamuserimages-a.akamaihd.net/ugc/2361643441471678039/F1F52E2F3D88F7D9B91C8CF4AEE8C60A4B781DD2/",
    ],
    949230: [
        "https://steamuserimages-a.akamaihd.net/ugc/2326739910484796550/69E99A8C05D8AB212B4CC3DB91EFE13F371E7523/",
        "https://steamuserimages-a.akamaihd.net/ugc/2323362510602309666/010AA9AFACB1661E4BA4FF6E93DD3D30B87FCF97/",
        "https://steamuserimages-a.akamaihd.net/ugc/2264814781720935897/A0BAB7B1BF9BA1196A513939CF37DB8E58449A87/",
        "https://steamuserimages-a.akamaihd.net/ugc/2304221912380183576/78A89FFB40E790FE8E1E5C196561FE3E5B9953B9/",
        "https://steamuserimages-a.akamaihd.net/ugc/2306473712165309858/7005F92D5F8226A9BC4A2FD6F057762811DF03F4/",
    ],
    70: [
        "https://steamuserimages-a.akamaihd.net/ugc/2334621843706320211/538A3CA57705E065EB56972302EE1B0B34F41839/",
        "https://steamuserimages-a.akamaihd.net/ugc/2325614010604770731/3EDDC47CBF59EB7774E9BF734A16AB784928839B/",
        "https://steamuserimages-a.akamaihd.net/ugc/2291837013354806713/465B4BF178D91EFA1640EC5DA7BB7B52416AA757/",
        "https://steamuserimages-a.akamaihd.net/ugc/2291837013354827873/03D6F5C355BA6261A8F88FC8D8B95A24ACB0500A/",
        "https://steamuserimages-a.akamaihd.net/ugc/2322236310850715876/7A38EC491E7B72004BE5FF2E6789D8F4C75C7A47/",
    ],
}
steam_file_id = 1


async def get_games(session: AsyncSession) -> list[Game]:
    games: list[Game] = []

    for steam_id in [524220, 264710, 427520, 949230, 70]:  # 니어 오토마타, 서브노티카, 팩토리오, 시티즈 스카이라인2, 하프라이프
        stmt = select(Game).where(Game.steam_id == steam_id).options(selectinload("*"))
        rs = await session.exec(stmt)
        games.append(rs.one())

    return games


async def seed_screenshots(session: AsyncSession, *, game: Game) -> list[GameScreenshot]:
    global steam_file_id

    assert game.id is not None

    screenshots = []

    for url in screenshot_urls[game.steam_id]:
        steam_file_id += 1

        screenshots.append(
            GameScreenshot(
                steam_file_id=steam_file_id,
                url=url,
                game_id=game.id,
            )
        )

    session.add_all(screenshots)

    await session.commit()
    return screenshots


async def seed_quiz(session: AsyncSession, *, screenshots: Sequence[GameScreenshot]) -> Quiz:
    quiz = Quiz()
    for s in screenshots:
        quiz.screenshots.append(s)
    session.add(quiz)

    await session.commit()
    await session.refresh(quiz)

    return quiz


async def seed():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        games = await get_games(session)

        for game in games:
            screenshots = await seed_screenshots(session, game=game)
            await seed_quiz(session, screenshots=screenshots)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
