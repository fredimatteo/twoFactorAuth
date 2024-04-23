from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config import database
from src.schemas import user_schema
from src.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[user_schema.UserResponseSchema])
def get_users(db: Session = Depends(database.get_db)):
    users = user_service.get_all_users(db)

    return users


@router.post("/create", status_code=201, response_model=user_schema.UserResponseSchema)
def create_user(src: user_schema.UserCreateSchema, db: Session = Depends(database.get_db)):
    user = user_service.create_user(db=db, user=src)

    db.commit()

    return user
    