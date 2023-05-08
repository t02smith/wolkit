from pydantic import BaseModel


class WakeableDeviceBase(BaseModel):
    alias: str
    mac_addr: str
    ip_addr: str


class WakeableDeviceCreate(WakeableDeviceBase):
    pass


class WakeableDevice(WakeableDeviceBase):
    id: int
    status: int

    class Config:
        orm_mode = True
