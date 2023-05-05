from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import db.watchers as wat_db
from lib.watchers import WatcherDevice

watchers_router = APIRouter(prefix="/watchers")


# types

class WatcherRequest(BaseModel):
    mac_addr: str
    ip_addr: str
    bluetooth: bool
    wireless: bool
    timeout_minutes: int


class WatcherResponse(BaseModel):
    mac_addr: str
    ip_addr: str
    bluetooth: bool
    wireless: bool
    wakes: List[str]
    timeout_minutes: int


def _watcher_to_watcher_respond(watcher: WatcherDevice) -> WatcherResponse:
    return WatcherResponse(**{
            **watcher.__dict__,
            "wakes": list(map(lambda d: d.alias, watcher.wakes))
        })


@watchers_router.get(
    "/all",
    status_code=200,
    description="Get the set of all watched devices",
    response_model=List[WatcherResponse],
    tags=["Watcher"],
    name="Get all Watchers"
)
def get_all_watchers():
    return list(map(
        lambda w: _watcher_to_watcher_respond(w),
        wat_db.get_all_watchers()))


@watchers_router.get(
    "/{watcher_id}",
    status_code=200,
    description="Get a single watcher using its id",
    response_model=WatcherResponse,
    tags=["Watcher"],
    name="Get Watcher by ID"
)
def get_watcher(watcher_id: int):
    res = wat_db.get_watcher_by_id(watcher_id)
    if res is None:
        raise HTTPException(status_code=404, detail=f"Watcher with id {watcher_id} not found")

    return res


@watchers_router.post(
    "/",
    status_code=201,
    description="Create a new watcher",
    response_model=WatcherResponse,
    tags=["Watcher"],
    name="Create a new watcher"
)
def new_watcher(watcher: WatcherRequest):
    return wat_db.create_watcher(WatcherDevice(**{
        **watcher.__dict__,
        "devices": []
    }))
