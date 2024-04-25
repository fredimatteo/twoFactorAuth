from fastapi import FastAPI

from src.api import routers
from src.config import database

app = FastAPI(
    title="two factor API",
    description="API for two factor authentication",
    version="0.0.1",
)


@app.get("/")
def root():
    return {"message": "Hello coder!"}


@app.get("/healthcheck")
def healthcheck():
    return {
        "app_status": "Ok",
        "db_status": database.healthcheck(),
    }


app.include_router(router=routers.main_router)
