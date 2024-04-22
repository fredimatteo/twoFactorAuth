from fastapi import APIRouter

from src.api.v1 import user_api

main_router = APIRouter()

main_router.include_router(user_api.router)
