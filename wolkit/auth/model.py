from sqlalchemy.orm import sessionmaker

from auth.oauth import pwd_context
from db.connection import Base
from sqlalchemy import Boolean, Column, Integer, String, event


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False, index=False)
    admin = Column(Boolean, nullable=False, index=False)


def insert_admin_user(target, connection, **kwargs):
    ses = sessionmaker(bind=connection)
    db = ses()

    user = User(username="admin", password=pwd_context.hash("admin"), admin=True)
    db.add(user)
    db.commit()
    db.refresh(user)


event.listen(User.__table__, "after_create", insert_admin_user)