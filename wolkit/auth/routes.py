from typing import Any
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from auth.token import *
from pydantic import BaseModel
from auth.model import User
from auth.err import *
from db.connection import get_db

auth_router = APIRouter(prefix="/auth")


class UserOut(BaseModel):
    id: int
    username: str


class UserUpdate(BaseModel):
    password: str


@auth_router.post(
    "/login",
    description="Login to an existing account",
    status_code=201,
    tags=["Users"]
)
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token({"sub": user.username})
    response.set_cookie(key="access_token", value=access_token, samesite="strict")
    return {"access_token": access_token, "token_type": "bearer", "user": UserOut(**user.__dict__)}


@auth_router.put(
    "/",
    description="Update your user details",
    status_code=200,
    tags=["Users"]
)
async def change_password(updated_user: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if pwd_context.verify(updated_user.password, user.password):
        raise DuplicatePasswordError()

    auth_db.update_user_password(user.id, updated_user.password, db)
    return {
        "message": "Password updated successfully"
    }
