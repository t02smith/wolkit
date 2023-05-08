from sqlalchemy.orm import Session

from auth.oauth import pwd_context
from db.connection import db_con, db_cursor
from auth.model import User as UserModel


def get_all_users(db: Session):
    return db.query(UserModel).all()


def get_user_by_username(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()


def update_user_password(user_id: int, password: str, db: Session):
    user: UserModel = db.query(UserModel).filter(UserModel.id == user_id).first()
    user.password = pwd_context.hash(password)
    db.commit()
    db.refresh(user)
