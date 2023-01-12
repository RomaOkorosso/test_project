from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TokenBase(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenUpdate(TokenBase):
    pass


class TokenInDBBase(TokenBase):
    id: int

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class Token(TokenInDBBase):
    pass


class TokenCreate(BaseModel):
    username: str | None = None


class TokenSave(TokenBase):
    updated_at: datetime = datetime.utcnow()


class PasswordReset(BaseModel):
    username: str
    old_password: str
    new_password: str
