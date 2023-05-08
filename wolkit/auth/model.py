from db.connection import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False, index=False)
    admin = Column(Boolean, nullable=False, index=False)
