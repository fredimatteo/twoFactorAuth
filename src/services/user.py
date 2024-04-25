import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import user_model as u_model
from src.schemas import user_schema as u_schema
from src.services.auth import hash_password


def get_all_users(db: Session, user: u_model.User, skip: int = 0, limit: int = 10):
    select_query = select(u_model.User).offset(skip).limit(limit).order_by(u_model.User.id)

    if not user.is_admin:
        select_query = select_query.where(u_model.User.id == int(user.id))

    return db.execute(select_query).scalars().all()


def get_user_by_username(db: Session, username: str) -> u_model.User:
    return db.execute(select(u_model.User).where(u_model.User.username == username)).scalars().first()


def create_user(db: Session, user: u_schema.UserCreateSchema):
    user_obj = u_model.User(**user.model_dump())

    user_obj.salt = uuid.uuid4().hex
    user_obj.password = hash_password(user_obj.password, user_obj.salt)

    db.add(user_obj)

    return user_obj

