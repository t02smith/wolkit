from starlette.responses import JSONResponse
from router.app import app
from services.err import *
from fastapi import Request


@app.exception_handler(ServiceNotFoundError)
async def service_not_found_handler(req: Request, exc: ServiceNotFoundError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(ServiceAlreadyEnabledError)
async def service_already_enabled(req: Request, exc: ServiceAlreadyEnabledError):
    return JSONResponse(
        status_code=400,
        content={"message", exc.args[0]}
    )


@app.exception_handler(ServiceAlreadyDisabledError)
async def service_already_disabled(req: Request, exc: ServiceAlreadyDisabledError):
    return JSONResponse(
        status_code=400,
        content={"message", exc.args[0]}
    )