from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.config import database
from src.config.database import SessionLocal
from src.models.user_model import User
from src.schemas import user_schema
from src.services import user as user_service, auth as auth_service

router = APIRouter(prefix="/users", tags=["users"])


security = HTTPBearer()


async def authenticate(credential: HTTPAuthorizationCredentials = Security(security)):
    try:
        db = SessionLocal()
        user = auth_service.decode_token(credential.credentials, db)
        return user
    except Exception as e:
        raise e


@router.get("", response_model=List[user_schema.UserResponseSchema])
def get_users(db: Session = Depends(database.get_db), current_user: User = Depends(authenticate)):
    users = user_service.get_all_users(db, current_user)

    return users


@router.post("/create", status_code=201, response_model=user_schema.UserResponseSchema)
def create_user(src: user_schema.UserCreateSchema, db: Session = Depends(database.get_db)):
    user = user_service.create_user(db=db, user=src)

    db.commit()

    return user
