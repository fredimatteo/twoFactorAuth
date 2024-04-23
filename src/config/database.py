from sqlalchemy import create_engine, text
from sqlalchemy import exc as alchemy_exceptions
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

st = settings.get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{st.db_user}:{st.db_password}@{st.db_host}:{st.db_port}/{st.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except alchemy_exceptions.DatabaseError as err:
        print("An exception occurred: {}".format(err))
        db.rollback()
    finally:
        db.close()


def healthcheck() -> str:
    db = SessionLocal()
    try:
        # Try to create a session and execute a simple query
        db.execute(text("SELECT 1"))
        return "Ok"
    except alchemy_exceptions.OperationalError:
        # If there's an error connecting to the database, return False
        return "Offline"
    finally:
        db.close()
