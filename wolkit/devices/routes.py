from fastapi import APIRouter, HTTPException

import wolkit.devices.errors
from wolkit.services.schedule.routes import schedules_router
from typing import List
from wolkit.devices.device import WakeableDevice
import wolkit.devices.db as dev_db
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
    response_model=List[WakeableDevice],
    summary="Returns a list of all recorded devices.",
    tags=["Device Management"])
async def get_all_devices() -> List[WakeableDevice]:
    return dev_db.get_all_devices()


@devices_router.post(
    "/",
    status_code=201,
    name="Create a New Device",
    description="Create a new device to track and use within this API",
    response_model=WakeableDevice,
    summary="Record a new device.",
    tags=["Device Management"])
async def create_new_device(device: WakeableDeviceRequest) -> WakeableDevice:
    try :
        return dev_db.new_device(WakeableDevice(**{
            **device.__dict__,
            "id": 0,
            "status": 2
        }))
    except devices.errors.DeviceDetailsAlreadyUsed as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@devices_router.post(
    "/wake",
    status_code=204,
    name="Wake a Device",
    description="Sends a magic packet over LAN to wake your device up from sleep mode. Remember your device will take "
                "time to boot up.",
    summary="Wake up one of your devices.",
    tags=["Device Management"]
)
async def wake_device(alias: str):
    device = dev_db.find_device_by_alias(alias)
    if device is None:
        raise HTTPException(status_code=404, detail=f"Device with alias '{alias}' not found.")

    device.wake()