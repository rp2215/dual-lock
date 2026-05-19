from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

# reads .env files
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # creates connection
SessionLocal = sessionmaker(bind=engine) # each request gets its own session


# used to track tables
# all models will inherit this
class Base(DeclarativeBase):
    pass

# opens session and hands it to route
def get_db():

    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
