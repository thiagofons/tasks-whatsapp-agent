import os

from app.persistance.models import *
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

# local stored database
DATABASE_URL = os.getenv("DATABASE_URL")

# in-memory database for testing
TEST_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False) \
    if os.getenv("ENV") != "test" else create_engine(TEST_DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


create_db_and_tables()