from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
import services.wireless.queries as wat_db
from auth.token import get_current_user
from auth.model import User
from db.connection import get_db
from services.wireless.schema import WatcherDevice as WatcherDeviceSchema, WatcherDeviceCreate, WatcherDevicePatch, \
    WatcherDeviceUpdate, WatcherDeviceMappingCreate

watchers_router = APIRouter(prefix="/watchers")


@watchers_router.get(
    "/all",
    status_code=200,
    description="Get the set of all watched devices",
    response_model=List[WatcherDeviceSchema],
    tags=["Watcher"],
    name="Get all Watchers"
)
async def get_all_watchers(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return wat_db.get_all_watchers(db)


@watchers_router.get(
    "/{watcher_id}",
    status_code=200,
    description="Get a single watcher using its id",
    response_model=WatcherDeviceSchema,
    tags=["Watcher"],
    name="Get Watcher by ID"
)
async def get_watcher(watcher_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return wat_db.get_watcher_by_id(watcher_id, db)


@watchers_router.post(
    "/",
    status_code=201,
    description="Create a new watcher by submitting some details about it. The bluetooth_mac_addr refers to your "
                "watcher device's unique bluetooth address and remembed it may be different from you Wi-Fi MAC "
                "address. Your lan_ip_addr refers to the device's IP address in the local network and for best "
                "results ensure that it is static. The timeout means that this device will only trigger devices to "
                "wake up once for every given time period, ",
    response_model=WatcherDeviceSchema,
    tags=["Watcher"],
    name="Create a new watcher"
)
async def new_watcher(watcher: WatcherDeviceCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return wat_db.create_watcher(watcher, db)


@watchers_router.put(
    "/{watcher_id}/watch",
    status_code=200,
    description="Map a watcher device to a wakeable device. When the watcher device is found via either wireless or "
                "bluetooth, it will turn on the target device.",
    tags=["Watcher"],
    name="Map Watcher to Target"
)
async def map_watcher_to_target(watcher_id: int, device_id: int, mapping: WatcherDeviceMappingCreate, user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    return wat_db.map_watcher_to_wakeable_device(watcher_id, device_id, mapping, db)


@watchers_router.delete(
    "/{watcher_id}/watch",
    status_code=204,
    description="Remove a mapping to a wakeable device from the given watcher device.",
    tags=["Watcher"],
    name="Removing mapping to wakeable device"
)
async def remove_mapping_to_wakeable_device(watcher_id: int, device_id: int, user: User = Depends(get_current_user),
                                            db: Session = Depends(get_db)):
    wat_db.remove_mapping(watcher_id, device_id, db)


@watchers_router.delete(
    "/{watcher_id}",
    status_code=204,
    description="Delete a watcher device and remove any mappings to target devices",
    tags=["Watcher"],
    name="Remove watcher device"
)
async def remove_watcher_device(watcher_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wat_db.remove_watcher(watcher_id, db)


@watchers_router.patch(
    "/{watcher_id}",
    status_code=200,
    description="Update an existing watcher",
    tags=["Watcher"],
    response_model=WatcherDeviceSchema,
    name="Patch watcher"
)
async def patch_watcher(watcher_id: int, update: WatcherDevicePatch, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return wat_db.patch_watcher(watcher_id, update, db)


@watchers_router.put(
    "/{watcher_id}",
    status_code=200,
    description="Patch an existing watcher. Here you can change any of the attributes for a given watcher by only "
                "supplying the ones you want to change. Omit any attributes that are not changed.",
    tags=["Watcher"],
    response_model=WatcherDeviceSchema,
    name="Update watcher"
)
async def update_watcher(watcher_id: int, update: WatcherDeviceUpdate, user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return wat_db.update_watcher(watcher_id, update, db)
