from router.app import app
from services.wireless.err import *
from fastapi import Request, HTTPException


@app.exception_handler(WatcherNotFoundError)
async def watcher_not_found_handler(req: Request, exc: WatcherNotFoundError):
    return HTTPException(
        status_code=404,
        detail=exc.args[0]
    )
