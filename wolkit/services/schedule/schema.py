from pydantic import BaseModel


class ScheduleBase(BaseModel):
    weekday: int
    hour: int
    minute: int


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    device_id: int
    id: int
    active: bool

    class Config:
        orm_mode = True
