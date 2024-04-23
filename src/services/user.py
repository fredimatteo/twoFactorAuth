from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from src.models import user_model as u_model


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    select_query = select(u_model.User).offset(skip).limit(limit).order_by(desc(u_model.User.id))

    return db.execute(select_query).scalars().all()
