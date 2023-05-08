from fastapi import APIRouter, Depends

from auth.token import get_current_user
from auth.user import User
from services.schedule import db as schedule_db
from pydantic import BaseModel
from services.schedule.schedule import Schedule
from typing import List

schedules_router = APIRouter(prefix="/{device_id}/schedule")


# request types

class ScheduleRequest(BaseModel):
    device: int
    weekday: int
    hour: int
    minute: int


#

@schedules_router.get(
    "/all",
    status_code=200,
    description="Get a list of all active schedules for a device",
    response_model=List[Schedule],
    name="Get Schedules by Device",
    tags=["Scheduler"])
async def get_all_schedules_for_device(device_id: int, user: User = Depends(get_current_user)) -> List[Schedule]:
    return schedule_db.get_schedules_for_device(device_id)


@schedules_router.post(
    "/",
    status_code=201,
    description="Add a new schedule for an existing device",
    response_model=Schedule,
    name="Create a scheduled wake-up",
    tags=["Scheduler"]
)
async def create_schedule(schedule: ScheduleRequest, user: User = Depends(get_current_user)) -> Schedule:
    s = Schedule(**{**schedule.__dict__, "id": -1})
    schedule_db.create_new_schedule(s)
    return s
