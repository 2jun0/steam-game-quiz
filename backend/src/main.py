from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.config import app_configs
from src.database import create_all_table
from src.quiz.router import router as quiz_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_table()


app = FastAPI(**app_configs, lifespan=lifespan)
app.add_api_route(quiz_router)
