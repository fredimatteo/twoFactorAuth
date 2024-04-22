from sqlalchemy import create_engine
from sqlalchemy import exc as alchemy_exceptions
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{database}"

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
        db.close()
