from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate, hashed_password: str):  # noqa
        obj_in.__delattr__("password")
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.hashed_password = hashed_password
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def activate_user(self, db: Session, user_id: int):
        db_user: User = db.query(self.model).get(user_id)
        db_user.disabled = False
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_by_token(self, db: Session, token_id: int):
        return db.query(self.model).filter(self.model.token_id == token_id).first()


user = CRUDUser(User)
