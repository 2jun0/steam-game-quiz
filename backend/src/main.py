from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.config import app_configs, settings
from src.game.router import router as game_router
from src.quiz.router import router as quiz_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(**app_configs, lifespan=lifespan)
app.include_router(quiz_router)
app.include_router(game_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
