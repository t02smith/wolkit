from router.app import app
from auth.err import *
from fastapi import Request, HTTPException


@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return HTTPException(
        status_code=400,
        detail=exc.args[0]
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return HTTPException(
        status_code=400,
        detail=exc.args[0]
    )


@app.exception_handler(InvalidTokenError)
async def invalid_user_credentials_handler(request: Request, exc: InvalidTokenError):
    return HTTPException(
        status_code=400,
        detail=exc.args[0]
    )
