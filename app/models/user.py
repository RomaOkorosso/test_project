from datetime import datetime
from sqlalchemy import Text, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text)
    full_name = Column(Text, nullable=False)
    email = Column(Text)
    hashed_password = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    token = relationship("Token")
    token_id = Column(Integer, ForeignKey("tokens.id"))

    posts = relationship("Post")
