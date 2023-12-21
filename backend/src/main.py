from fastapi import FastAPI
from src.config import app_configs


app = FastAPI(**app_configs)
