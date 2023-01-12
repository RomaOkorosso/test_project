from datetime import datetime
from sqlalchemy import Text, Integer, Column, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

user_likes = Table(
    "user_likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
)
user_dislikes = Table(
    "user_dislikes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    text = Column(Text)
    likes = relationship("User", secondary=user_likes, back_populates="posts")
    dislikes = relationship("User", secondary=user_dislikes, back_populates="posts")

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
