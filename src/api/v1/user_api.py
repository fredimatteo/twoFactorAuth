from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config import database
from src.config import exception
from src.config.middleware.auth_middleware import authenticate
from src.models.user_model import User
from src.schemas import user_schema
from src.services import user_service, auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[user_schema.UserResponseSchema])
def get_users(db: Session = Depends(database.get_db), current_user: User = Depends(authenticate)):
    users = user_service.get_all_users(db, current_user)

    return users


@router.post("/create", status_code=201, response_model=user_schema.VerifyEmailResponseSchema)
def create_user(src: user_schema.UserCreateSchema, db: Session = Depends(database.get_db)):
    user = user_service.get_user_by_username(db=db, username=src.username)
    if user:
        raise exception.BadRequestException(message=f"User {src.username} already exists")

    user = user_service.create_user(db=db, user=src)

    temp_token = auth_service.generate_temporary_token()
    user.mail_validation_token = temp_token

    db.commit()

    return user_schema.VerifyEmailResponseSchema(email=user.email, token=temp_token)
