from sqlalchemy.orm import Session
from auth.err import UserNotFoundError
from auth.oauth import pwd_context
from auth.model import User as UserModel


def get_all_users(db: Session):
    return db.query(UserModel).all()


def get_user_by_username(username: str, db: Session):
    return db.query(UserModel).filter_by(username=username).first()


def update_user_password(user_id: int, password: str, db: Session):
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise UserNotFoundError(user_id)

    user.password = pwd_context.hash(password)
    db.commit()
    db.refresh(user)
