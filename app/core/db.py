from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from app.core.config import config

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


def get_db():
    session = Session(bind=engine, autoflush=False, autocommit=False)
    try:
        yield session
    finally:
        session.close()
