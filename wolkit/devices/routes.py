from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from auth.token import get_current_user
from auth.model import User
from db.connection import get_db
from services.schedule.routes import schedules_router
from typing import List
from devices.schema import WakeableDeviceCreate
from devices.model import WakeableDevice as WakeableDeviceModel
import devices.queries as dev_db
from pydantic import BaseModel


devices_router = APIRouter(prefix="/devices")
devices_router.include_router(schedules_router)


class WakeableDeviceRequest(BaseModel):
    alias: str
    mac_addr: str
    ip_addr: str


@devices_router.get(
    "/all",
    status_code=200,
    name="Get All Devices",
    description="Get a list of all your recorded devices. These devices can be woken up by this API.",
    summary="Returns a list of all recorded devices.",
    tags=["Device Management"])
async def get_all_devices(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return dev_db.get_all_devices(db)


@devices_router.get(
    "/{device_id}",
    status_code=200,
    name="Get a device",
    description="Get an existing device using its unique ID",
    summary="Get an existing device",
    tags=["Device Management"]
)
async def delete_device(device: WakeableDeviceModel = Depends(dev_db.get_device_by_id), user: User = Depends(get_current_user)):
    return device


@devices_router.post(
    "/",
    status_code=201,
    name="Create a New Device",
    description="Create a new device to track and use within this API",
    summary="Record a new device.",
    tags=["Device Management"])
async def create_new_device(device: WakeableDeviceCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return dev_db.new_device(device, db)


@devices_router.post(
    "/{device_id}/wake",
    status_code=204,
    name="Wake a Device",
    description="Sends a magic packet over LAN to wake your device up from sleep mode. Remember your device will take "
                "time to boot up.",
    summary="Wake up one of your devices.",
    tags=["Device Management"]
)
async def wake_device(device: WakeableDeviceModel = Depends(dev_db.get_device_by_id), user: User = Depends(get_current_user)):
    device.wake()


@devices_router.delete(
    "/{device_id}",
    status_code=204,
    name="Delete a device",
    description="Delete an existing device and any references to it",
    summary="Delete an existing device",
    tags=["Device Management"]
)
async def delete_device(device: WakeableDeviceModel = Depends(dev_db.get_device_by_id), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dev_db.delete_device(device.id, db)
