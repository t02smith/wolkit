from router.app import app
from devices.err import *
from fastapi import Request, HTTPException


@app.exception_handler(DeviceDetailsAlreadyUsed)
async def device_details_in_use_handler(request: Request, exc: DeviceDetailsAlreadyUsed):
    return HTTPException(
        status_code=400,
        detail=exc.args[0]
    )


@app.exception_handler(DeviceNotFoundError)
async def device_not_found_handler(request: Request, exc: DeviceNotFoundError):
    return HTTPException(
        status_code=400,
        detail=exc.args[0]
    )
