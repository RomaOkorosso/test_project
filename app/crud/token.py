from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import Token
from app.schemas import (
    TokenSave,
    TokenUpdate,
)


class CRUDToken(CRUDBase[Token, TokenSave, TokenUpdate]):
    def get_by_access_token(self, db: Session, access_token: str):
        return (
            db.query(self.model).filter(self.model.access_token == access_token).first()
        )


token = CRUDToken(Token)
