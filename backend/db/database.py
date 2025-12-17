from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

# create connection to database
engine = create_engine(settings.DATABASE_URL)

# generate new database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# tables inherit from this
Base = declarative_base()


# insures we do not have more than one session
def get_db():
    # instantiate new session
    db = SessionLocal()
    try:
        # suspend function and retrieve values one at a time
        yield db
        # close databse
    finally:
        db.close()


# create corresponding tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)
