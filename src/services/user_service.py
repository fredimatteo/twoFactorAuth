import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import exception
from src.models import user_model as u_model
from src.schemas import user_schema as u_schema
from src.services.auth_service import hash_password


def get_all_users(db: Session, user: u_model.User, skip: int = 0, limit: int = 10):
    select_query = select(u_model.User).offset(skip).limit(limit).order_by(u_model.User.id)

    if not user.is_admin:
        select_query = select_query.where(u_model.User.id == int(user.id))

    return db.execute(select_query).scalars().all()


def get_user_by_username(db: Session, username: str) -> u_model.User:
    return db.execute(select(u_model.User).where(u_model.User.username == username)).scalars().first()


def get_user_by_otp_validation_token(db: Session, validation_token: str) -> u_model.User:
    select_query = select(u_model.User).where(u_model.User.otp_validation_token == validation_token)

    user = db.execute(select_query).scalars().first()

    if user is None:
        raise exception.NotFoundException("with provided otp token")

    return user


def create_user(db: Session, user: u_schema.UserCreateSchema, otp_secret: str):
    user_obj = u_model.User(**user.model_dump())

    user_obj.salt = uuid.uuid4().hex
    user_obj.password = hash_password(user_obj.password, user_obj.salt)
    user_obj.otp_secret = otp_secret

    db.add(user_obj)

    return user_obj


def update_user_otp_token(db: Session, otp_validation_token: str | None, user_id: int):
    select_query = select(u_model.User).where(u_model.User.id == user_id)

    user = db.execute(select_query).scalars().first()

    if user is None:
        raise exception.NotFoundException(None)

    user.otp_validation_token = otp_validation_token
    db.add(user)
