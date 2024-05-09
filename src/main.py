from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import routers
from src.config import database
from src.config import exception

app = FastAPI(
    title="two factor API",
    description="API for two factor authentication",
    version="0.0.1",
)

app.add_exception_handler(exception.NotFoundException, exception.not_found_exception_handler)
app.add_exception_handler(exception.InvalidCredentialsException, exception.invalid_credentials_exception_handler)
app.add_exception_handler(exception.GenericException, exception.generic_exception_handler)
app.add_exception_handler(exception.BadRequestException, exception.bad_request_exception_handler)

origins = [
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
