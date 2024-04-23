import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import user_model as u_model
from src.schemas import user_schema as u_schema


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    # TODO@1 implement this data from JWT
    is_admin = False
    u_id = 1

    select_query = select(u_model.User).offset(skip).limit(limit).order_by(u_model.User.id)

    if not is_admin:
        select_query = select_query.where(u_model.User.id == u_id)

    return db.execute(select_query).scalars().all()


def create_user(db: Session, user: u_schema.UserCreateSchema):
    user_obj = u_model.User(**user.model_dump())

    user_obj.salt = uuid.uuid4().hex
    user_obj.password = __hash_password(user_obj.password, user_obj.salt)

    db.add(user_obj)

    return user_obj


def __hash_password(password, salt):
    return password + salt + "hashed"
