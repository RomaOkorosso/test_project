import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from app import schemas, crud, models
from app.core.config import settings
from app.dependencies import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> str:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        db_user = crud.user.get_by_username(db=db, username=username)
        if not db_user:
            return None
        if not auth.verify_password(password, db_user.hashed_password):
            return None
        return db_user

    @staticmethod
    def create_access_token(
        db: Session,
        data: dict,
        expires_delta: Optional[timedelta] = timedelta(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        db_token = crud.token.create(
            db=db,
            obj_in=schemas.TokenSave(
                access_token=encoded_jwt,
            ),
        )
        auth.update_token_in_db(db=db, db_token=db_token, username=to_encode.get("sub"))

        return encoded_jwt

    @staticmethod
    def update_token_in_db(db: Session, username: str, db_token: models.Token):
        db_user = crud.user.get_by_username(db=db, username=username)

        old_token: models.Token = db_user.token
        if old_token:
            db_user.token = None
            db_user.token_id = None
            db.commit()
            db.flush()
            crud.token.remove(db=db, id=old_token.id)

        db_user.token = db_token
        db_user.token_id = db_token.id
        db.commit()
        db.refresh(db_user)

    @staticmethod
    def get_current_user(token: str, db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        new_token = None

        try:
            # Will raise an exception if token is expired
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception

            expiration_date = payload.get("exp")
            expiration_date = datetime.utcfromtimestamp(expiration_date)

            # Check if it's time to update the token
            if datetime.utcnow() < expiration_date:
                new_token = auth.create_access_token(
                    db=db,
                    data={"sub": username},
                )

        except JWTError:
            raise credentials_exception

        token = new_token if new_token else token
        db_user = crud.user.get_by_token(db=db, token_id=token)

        if db_user is None:
            raise credentials_exception

        return db_user, token

    @staticmethod
    def generate_new_password(username: str, db: Session):
        new_password = secrets.token_hex(6)

        db_user = crud.user.get_by_username(db=db, username=username)

        if not db_user:
            raise HTTPException(404, "User does not exist")

        db_user.hashed_password = auth.get_password_hash(new_password)

        db.commit()
        db.refresh(db_user)
        return new_password

    @staticmethod
    def get_user_by_token(token: str, db: Session):
        db_token = crud.token.get_by_access_token(db=db, access_token=token)
        db_user = crud.user.get_by_token(db=db, token_id=db_token.id)
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid token")
        return db_user


auth = Auth()
