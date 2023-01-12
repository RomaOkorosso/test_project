from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.exceptions import UnexpectedError, InvalidOperation, InvalidUser
from app.schemas import PostCreate
from app.services import auth as auth_methods


class Post:
    @staticmethod
    def get_all_posts(db: Session) -> list[models.Post]:
        try:
            posts = crud.post.get_all(db=db)
        except Exception as e:
            print("Could not get all posts: {}".format(e))
            raise UnexpectedError
        return posts

    @staticmethod
    def add_post(db: Session, token: str, new_post: PostCreate):
        db_token = crud.token.get_by_access_token(db=db, access_token=token)
        db_user = crud.user.get_by_token(db=db, token_id=db_token.id)

        db_post = crud.post.create(db=db, obj_in=new_post)

        db_post = crud.post.add_user_to_post(db=db, db_user=db_user, db_post=db_post)

        return db_post

    @staticmethod
    def get_post_by_id(db: Session, post_id: int):
        return crud.post.get(db=db, id=post_id)

    @staticmethod
    def add_mark_to_post(db: Session, token: str, post_id: int, like: bool = True):
        db_token = crud.token.get_by_access_token(db=db, access_token=token)
        db_user = crud.user.get_by_token(db=db, token_id=db_token.id)
        try:
            db_post = crud.post.add_mark(
                db=db, user_id=db_user.id, post_id=post_id, like=like
            )
        except InvalidOperation:
            raise InvalidOperation()
        return db_post

    @staticmethod
    def update_post_by_id(
        db: Session, post_id: int, token: str, upd_post: schemas.PostUpdate
    ):
        db_token = crud.token.get_by_access_token(db=db, access_token=token)
        db_user = crud.user.get_by_token(db=db, token_id=db_token.id)
        db_post = crud.post.get(db=db, id=post_id)

        if db_post.user_id != db_user.id:
            raise InvalidUser("You are not an author of post")

        db_post = crud.post.update(db=db, db_obj=db_post, obj_in=upd_post)
        return db_post

    @staticmethod
    def delete_post_by_id(db: Session, post_id: int, token: str) -> bool:
        db_token = crud.token.get_by_access_token(db=db, access_token=token)
        db_user = crud.user.get_by_token(db=db, token_id=db_token.id)
        db_post = crud.post.get(db=db, id=post_id)

        if db_post.user_id != db_user.id:
            raise InvalidUser("You are not an author of post")

        try:
            crud.post.remove(db=db, id=db_post.id)
        except Exception as err:
            print("Error while removing post from database: ", err)
            return False
        return True


post = Post()
