from typing import Optional

from pydantic import BaseModel


class WakeableDeviceBase(BaseModel):
    alias: str
    mac_addr: str
    ip_addr: str


class WakeableDeviceCreate(WakeableDeviceBase):
    pass


class WakeableDevicePatch(BaseModel):
    alias: Optional[str] = None
    mac_addr: Optional[str] = None
    ip_addr: Optional[str] = None


class WakeableDeviceUpdate(WakeableDeviceBase):
    pass


class WakeableDevice(WakeableDeviceBase):
    id: int
    status: int

    class Config:
        orm_mode = True
