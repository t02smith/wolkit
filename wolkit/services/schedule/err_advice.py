from router.app import app
from fastapi import Request
from services.schedule.err import *
from fastapi.responses import JSONResponse


@app.exception_handler(ScheduleNotFoundError)
async def schedule_not_found_error(req: Request, exc: ScheduleNotFoundError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(ScheduleAlreadyEnabledError)
async def schedule_already_enabled_error(req: Request, exc: ScheduleAlreadyEnabledError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )


@app.exception_handler(ScheduleAlreadyDisabledError)
async def schedule_already_disabled_error(req: Request, exc: ScheduleAlreadyDisabledError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.args[0]}
    )
