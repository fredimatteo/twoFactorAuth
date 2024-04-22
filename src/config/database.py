from sqlalchemy import create_engine
from sqlalchemy import exc as alchemy_exceptions
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.main import get_settings

st = get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{st.db_user}:{st.db_password}@{st.db_host}:{st.db_port}/{st.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except alchemy_exceptions.SQLAlchemyError as err:
        print("An exception occurred: {}".format(err))
        db.rollback()
    finally:
        db.close()
