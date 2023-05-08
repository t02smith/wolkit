from starlette.responses import JSONResponse

from router.app import app
from auth.err import *
from fastapi import Request


@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(InvalidUserCredentials)
async def invalid_user_credentials_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(DuplicatePasswordError)
async def duplicate_password_handler(request: Request, exc: DuplicatePasswordError):
    return JSONResponse(
        status_code=400,
        content={"message": "Your new password must be different from your old password"}
    )
