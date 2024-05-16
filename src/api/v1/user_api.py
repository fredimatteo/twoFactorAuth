from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config import database
from src.config.exception import GenericException, BadRequestException
from src.config.middleware.auth_middleware import authenticate
from src.models.user_model import User
from src.schemas import user_schema
from src.services import user_service, auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get(path="", response_model=List[user_schema.UserResponseSchema])
def get_users(db: Session = Depends(database.get_db), current_user: User = Depends(authenticate)):
    try:
        users = user_service.get_all_users(db, current_user)
        return users
    except Exception as e:
        raise GenericException(str(e))


@router.post(path="/create", status_code=status.HTTP_201_CREATED, response_model=user_schema.VerifyEmailResponseSchema)
def create_user(src: user_schema.UserCreateSchema, db: Session = Depends(database.get_db)):
    try:
        user = user_service.get_user_by_username(db=db, username=src.username)
        if user:
            raise BadRequestException(message=f"User {src.username} already exists")

        user = user_service.create_user(db=db, user=src)

        temp_token = auth_service.generate_temporary_token()
        user.mail_validation_token = temp_token

        db.commit()
        return user_schema.VerifyEmailResponseSchema(email=user.email, token=temp_token)
    except BadRequestException as e:
        raise BadRequestException(str(e)) from e
    except Exception as e:
        raise GenericException(str(e)) from e
