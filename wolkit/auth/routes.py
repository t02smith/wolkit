from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from wolkit.auth.token import *

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
