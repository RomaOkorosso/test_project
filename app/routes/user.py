from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db
from app.routes.auth import oauth2_scheme
from app.services import auth

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=schemas.UserInDB)
async def get_me(_: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db_user = auth.get_user_by_token(db=db, token=_)
    return db_user
