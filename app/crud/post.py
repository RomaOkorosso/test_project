from sqlalchemy.orm import Session
from app.exceptions import InvalidOperation
from app.models import Post, user_likes, user_dislikes, User
from app.schemas import PostCreate, PostUpdate
from app.crud.base import CRUDBase


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def add_mark(self, db: Session, user_id: int, post_id: int, like: bool = True):
        db_post = self.get(db=db, id=post_id)

        if db_post.user_id == user_id:  # if author try to add mark on own post
            raise InvalidOperation()
        if like:
            db_mark = (
                db.query(user_likes)
                .filter(post_id == post_id and user_id == user_id)
                .first()
            )
        else:
            db_mark = (
                db.query(user_dislikes)
                .filter(post_id == post_id and user_id == user_id)
                .first()
            )

        if db_mark:
            query = (
                user_likes.delete().where(post_id == post_id).where(user_id == user_id)
            )
            db.execute(query)
            db.commit()
            db.refresh(db_post)
            return db_post

        if like:
            query = user_likes.insert().values(post_id=post_id, user_id=user_id)
        else:
            query = user_dislikes.insert().values(post_id=post_id, user_id=user_id)

        db.execute(query)
        db.commit()
        db.refresh(db_post)

        return db_post

    def add_user_to_post(self, db: Session, db_user: User, db_post: Post):
        db_post.user_id = db_user.id
        db.commit()
        db.refresh(db_post)

        return db_post


post = CRUDPost(Post)
