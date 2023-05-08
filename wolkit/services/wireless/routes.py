from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from sqlalchemy.orm import Session

import services.wireless.queries as wat_db
from auth.token import get_current_user
from auth.model import User
from db.connection import get_db
from services.wireless.model import WatcherDevice as WatcherDeviceModel
from services.wireless.schema import WatcherDevice as WatcherDeviceSchema, WatcherDeviceCreate

watchers_router = APIRouter(prefix="/watchers")


# types

class WatcherRequest(BaseModel):
    mac_addr: str
    ip_addr: str
    bluetooth: bool
    wireless: bool
    timeout_minutes: int



@watchers_router.get(
    "/all",
    status_code=200,
    description="Get the set of all watched devices",
    response_model=List[WatcherDeviceSchema],
    tags=["Watcher"],
    name="Get all Watchers"
)
def get_all_watchers(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return wat_db.get_all_watchers(db)


@watchers_router.get(
    "/{watcher_id}",
    status_code=200,
    description="Get a single watcher using its id",
    response_model=WatcherDeviceSchema,
    tags=["Watcher"],
    name="Get Watcher by ID"
)
def get_watcher(watcher_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return wat_db.get_watcher_by_id(watcher_id, db)


@watchers_router.post(
    "/",
    status_code=201,
    description="Create a new watcher",
    response_model=WatcherDeviceSchema,
    tags=["Watcher"],
    name="Create a new watcher"
)
def new_watcher(watcher: WatcherDeviceCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return wat_db.create_watcher(watcher, db)
