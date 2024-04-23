from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config import database
from src.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_users(db: Session = Depends(database.get_db)):
    users = user_service.get_all_users(db)

    return users
