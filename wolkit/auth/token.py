from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import Depends
from auth.oauth import *
from auth.user import User
import auth.db as auth_db
import auth.errors as auth_err


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


def compare_password(given: str, expected_hash: str) -> bool:
    return pwd_context.verify(given, expected_hash)


def create_access_token(data: dict, expires_in: Union[timedelta, None] = None):
    to_encode = data.copy()
    expires = datetime.utcnow() + expires_in if expires_in else datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_token(token: str = Depends(oauth2)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise auth_err.InvalidTokenError("Invalid token given")

        token_data = TokenData(username=username)
    except JWTError:
        raise auth_err.InvalidTokenError("Invalid token given")

    user = auth_db.get_user_by_username(username)
    if user is None:
        raise auth_err.UserNotFoundError(f"User with username {username} not found")
    return user


def authenticate_user(username: str, password: str) -> User:
    user = auth_db.get_user_by_username(username)
    if user is None:
        raise auth_err.UserNotFoundError(f"User with username {username} not found")

    if not compare_password(password, user.password):
        raise auth_err.InvalidUserCredentials("Invalid password")

    return user
