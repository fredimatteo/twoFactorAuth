from functools import lru_cache

from fastapi import FastAPI
from src.api import routers

from src.config.settings import Settings

app = FastAPI(
    title="two factor API",
    description="API for two factor authentication",
    version="0.0.1",

)


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file='.env')


@app.get("/")
def root():
    return {"message": "Hello coder!"}


app.include_router(router=routers.main_router)
