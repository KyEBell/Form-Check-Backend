import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from app.models.video import Video
from app.models.tag import Tag
from app.models.user import User
from app.models.user_stats import UserStats

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
