from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator


class DBPost(BaseModel):
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


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None


class UserCreate(UserBase):
    password: str
    updated_at: datetime = datetime.utcnow()


# Properties to receive via API on update
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    token_id = Optional[int]

    class Config:
        arbitrary_types_allowed = True


class UserInDBBase(UserBase):
    id: int

    hashed_password: str
    created_at: datetime
    updated_at: datetime
    token_id: Optional[int]

    posts: list[DBPost]

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    pass
