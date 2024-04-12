from typing import Annotated

from fastapi import Depends

from .manager import RankScoreManager


async def get_rank_score_manager() -> RankScoreManager:
    return RankScoreManager()


RankScoreManagerDep = Annotated[RankScoreManager, Depends(get_rank_score_manager)]
