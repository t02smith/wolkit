from starlette.responses import JSONResponse

from router.app import app
from devices.err import *
from fastapi import Request, HTTPException


@app.exception_handler(DeviceDetailsAlreadyUsed)
async def device_details_in_use_handler(request: Request, exc: DeviceDetailsAlreadyUsed):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(DeviceNotFoundError)
async def device_not_found_handler(request: Request, exc: DeviceNotFoundError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )
