from typing import Union, List, Optional
from devices.schema import WakeableDevice

from pydantic import BaseModel


class WatcherDeviceBase(BaseModel):
    mac_addr: str
    bluetooth: bool
    ip_addr: str
    lan: bool
    timeout_minutes: int


class WatcherDeviceCreate(WatcherDeviceBase):
    pass


class WatcherDeviceUpdate(WatcherDeviceBase):
    pass


class WatcherDevicePatch(BaseModel):
    mac_addr: Optional[str] = None
    bluetooth: Optional[bool] = None
    ip_addr: Optional[str] = None
    lan: Optional[bool] = None
    timeout_minutes: Optional[int] = None


class WatcherDevice(WatcherDeviceBase):
    id: int
    last_checked: Union[int, None] = None
    wakes: List[WakeableDevice]

    class Config:
        orm_mode = True


class WatcherDeviceMapping(BaseModel):
    watcher_device: WatcherDevice
    wake_device: WakeableDevice
