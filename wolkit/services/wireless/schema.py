from typing import Union

from pydantic import BaseModel


class WatcherDeviceBase(BaseModel):
    mac_addr: str
    bluetooth: bool
    ip_addr: str
    lan: bool
    timeout_minutes: int


class WatcherDeviceCreate(WatcherDeviceBase):
    pass


class WatcherDevice(WatcherDeviceBase):
    id: int
    last_checked: Union[int, None] = None

    class Config:
        orm_mode = True
