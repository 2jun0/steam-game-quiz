from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.config import app_configs
from src.game.router import router as game_router
from src.quiz.router import router as quiz_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(**app_configs, lifespan=lifespan)
app.include_router(quiz_router)
app.include_router(game_router)
