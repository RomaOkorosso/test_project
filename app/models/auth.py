from datetime import datetime
from sqlalchemy import Text, Integer, Column, DateTime
from app.db.base import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(Text)
    token_type = Column(Text, default="bearer")
    updated_at = Column(DateTime, default=datetime.utcnow)
