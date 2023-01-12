from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.exceptions import UnexpectedError, InvalidOperation, InvalidUser
from app.routes.auth import oauth2_scheme
from app.services import post
from app.dependencies import get_db

router = APIRouter(prefix="/post", tags=["post"])


@router.get("/", response_model=list[schemas.PostInDB])
async def get_all_posts(db: Session = Depends(get_db), _=Depends(oauth2_scheme)):
    try:
        return post.get_all_posts(db)
    except UnexpectedError:
        raise UnexpectedError("Couldn't get all posts")
    except Exception as e:
        raise UnexpectedError("Unexpected error")


@router.post("/", response_model=schemas.PostInDB)
async def add_post(
    new_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    _=Depends(oauth2_scheme),
):
    db_post: models.Post = post.add_post(db=db, token=_, new_post=new_post)
    return db_post


@router.get("/<post_id>", response_model=schemas.PostInDB)
async def get_post_by_id(
    post_id: int, db: Session = Depends(get_db), _=Depends(oauth2_scheme)
):
    return post.get_post_by_id(db=db, post_id=post_id)


@router.patch("/<post_id>", response_model=schemas.PostInDB)
async def update_post_by_id(
    post_id: int,
    update_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    _=Depends(oauth2_scheme),
):
    try:
        db_post = post.update_post_by_id(
            db=db, post_id=post_id, token=_, upd_post=update_post
        )
    except InvalidUser as e:
        raise HTTPException(
            status_code=400,
            detail=e.args[0],
        )
    return db_post


@router.delete("/<post_id>")
async def delete_post(
    post_id: int, db: Session = Depends(get_db), _=Depends(oauth2_scheme)
):
    if post.delete_post_by_id(db=db, post_id=post_id, token=_):
        return {"detail": "deleted"}
    else:
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.get("/<post_id>/like", response_model=schemas.PostInDB)
async def add_like_to_post(
    post_id: int, db: Session = Depends(get_db), _=Depends(oauth2_scheme)
):
    try:
        db_post = post.add_mark_to_post(db=db, token=_, post_id=post_id)
    except InvalidOperation:
        raise HTTPException(status_code=400, detail="Could not like own posts")
    return db_post


@router.get("/<post_id>/dislike", response_model=schemas.PostInDB)
async def add_like_to_post(
    post_id: int, db: Session = Depends(get_db), _=Depends(oauth2_scheme)
):
    try:
        db_post = post.add_mark_to_post(db=db, token=_, post_id=post_id, like=False)
    except InvalidOperation:
        raise HTTPException(status_code=400, detail="Could not dislike own posts")
    return db_post
