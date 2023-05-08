from starlette.responses import JSONResponse

from router.app import app
from services.wireless.err import *
from fastapi import Request


@app.exception_handler(WatcherNotFoundError)
async def watcher_not_found_handler(req: Request, exc: WatcherNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.args[0]}
    )
