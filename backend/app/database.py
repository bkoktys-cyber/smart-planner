import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


def get_db():
    """Открывает сессию с БД на время запроса и закрывает её после."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()