from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, validator


class BasePost(BaseModel):
    title: str
    description: str
    text: str


class PostCreate(BasePost):
    pass


class PostUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    text: Optional[str]


class PostInDBBase(BasePost):
    id: int
    user_id: int

    likes: Any
    dislikes: Any

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @validator("likes")
    def set_likes(cls, v):
        if type(v) == int:
            return v
        return len(v)

    @validator("dislikes")
    def set_dislikes(cls, v):
        if type(v) == int:
            return v
        return len(v)


class PostInDB(PostInDBBase):
    pass
