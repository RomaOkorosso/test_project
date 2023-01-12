from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
