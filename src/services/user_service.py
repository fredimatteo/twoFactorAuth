import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config.exception import NotFoundException
from src.models import user_model as u_model
from src.schemas import user_schema as u_schema
from src.services import auth_service


def get_all_users(db: Session, user: u_model.User, skip: int = 0, limit: int = 10):
    select_query = select(u_model.User).offset(skip).limit(limit).order_by(u_model.User.id)

    if not user.is_admin:
        select_query = select_query.where(u_model.User.id == int(user.id))

    return db.execute(select_query).scalars().all()


def get_user_by_username(db: Session, username: str) -> u_model.User | None:
    select_query = select(u_model.User).where(u_model.User.username == username)

    user = db.execute(select_query).scalars().first()
    return user


def get_user_by_otp_validation_token(db: Session, validation_token: str) -> u_model.User:
    select_query = select(u_model.User).where(u_model.User.otp_validation_token == validation_token)

    user = db.execute(select_query).scalars().first()

    if user is None:
        raise NotFoundException("with provided otp token")

    return user


def get_user_by_email_validation_token(db: Session, validation_token: str) -> u_model.User:
    select_query = select(u_model.User).where(u_model.User.mail_validation_token == validation_token)

    user = db.execute(select_query).scalars().first()

    if user is None:
        raise NotFoundException("with provided mail validation token")

    return user


def create_user(db: Session, user: u_schema.UserCreateSchema):
    user_obj = u_model.User(**user.model_dump())

    user_obj.salt = uuid.uuid4().hex
    user_obj.password = auth_service.hash_password(user_obj.password, user_obj.salt)
    user_obj.disabled = True

    db.add(user_obj)

    return user_obj


def update_user_otp_token(db: Session, otp_validation_token: str | None, user_id: int) -> None:
    select_query = select(u_model.User).where(u_model.User.id == user_id)
    user = db.execute(select_query).scalars().first()

    if user is None:
        raise NotFoundException(None)

    user.otp_validation_token = otp_validation_token

    db.add(user)
