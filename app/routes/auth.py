from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app import schemas, crud
from app.dependencies import get_db
from app.services import auth

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(db=db, data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.UserInDB)
async def register(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    found_user = crud.user.get_by_username(db=db, username=new_user.username)

    if found_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    new_user = crud.user.create(
        db=db,
        obj_in=new_user,
        hashed_password=auth.get_password_hash(password=new_user.password),
    )

    return new_user


@router.get("/auth", response_model=schemas.UserInDB)
async def authenticate(
    response: Response,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user, token = auth.get_current_user(db, token)
    if token:
        response.set_cookie(key="Authorization", value=token)
    return user


@router.post("/get-forget-password")
async def get_new_password(username: str, db: Session = Depends(get_db)):
    new_password = auth.generate_new_password(db=db, username=username)

    return {"new_password": new_password}


@router.post("/reset-password", response_model=schemas.UserInDB)
async def reset_password(
    password_reset: schemas.PasswordReset,
    db: Session = Depends(get_db),
):
    db_user = crud.user.get_by_username(db=db, username=password_reset.username)

    if not db_user:
        raise HTTPException(404, "User does not exist")

    if auth.verify_password(password_reset.old_password, db_user.hashed_password):
        db_user.hashed_password = auth.get_password_hash(password_reset.new_password)

        db.commit()
        db.flush()

        return db_user
    else:
        raise HTTPException(400, "Passwords do not match")
