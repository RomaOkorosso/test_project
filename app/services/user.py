from sqlalchemy.orm import Session
from app import crud


class User:
    @staticmethod
    def is_user_exists(db: Session, user_id: int = None, username: str = None) -> bool:
        db_user = None

        if user_id:
            db_user = crud.user.get(db=db, id=user_id)
        elif username:
            db_user = crud.user.get_by_username(db=db, username=username)

        return db_user or False


user = User()
