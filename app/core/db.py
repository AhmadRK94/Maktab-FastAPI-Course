from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from app.core.config import settings

engine = create_engine(url=settings.SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


def get_db():
    session = Session(bind=engine, autoflush=False, autocommit=False)
    try:
        yield session
    finally:
        session.close()
