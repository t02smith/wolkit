from typing import Union, List, Optional
from devices.schema import WakeableDevice

from pydantic import BaseModel


class WatcherDeviceBase(BaseModel):
    bluetooth_mac_addr: str
    lan_ip_addr: str
    timeout_minutes: int


class WatcherDeviceCreate(WatcherDeviceBase):
    pass


class WatcherDeviceUpdate(WatcherDeviceBase):
    pass


class WatcherDevicePatch(BaseModel):
    bluetooth_mac_addr: Optional[str] = None
    lan_ip_addr: Optional[str] = None
    timeout_minutes: Optional[int] = None


class WatcherDevice(WatcherDeviceBase):
    id: int
    last_checked: Union[int, None] = None

    class Config:
        orm_mode = True


class WatcherDeviceMappingBase(BaseModel):
    bluetooth: bool
    lan: bool
    sniff_traffic: bool


class WatcherDeviceMappingCreate(WatcherDeviceMappingBase):
    pass


class WatcherDeviceMapping(WatcherDeviceMappingBase):
    watches: WatcherDevice
    wakes: WakeableDevice

    class Config:
        orm_mode = True


class WatcherDeviceMappingUpdate(WatcherDeviceMappingBase):
    pass
