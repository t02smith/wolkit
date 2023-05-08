from fastapi import APIRouter
from wolkit.services.schedule import db as schedule_db
from pydantic import BaseModel
from wolkit.services.schedule.schedule import Schedule
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
async def get_all_schedules_for_device(device_id: int) -> List[Schedule]:
    return schedule_db.get_schedules_for_device(device_id)


@schedules_router.post(
    "/",
    status_code=201,
    description="Add a new schedule for an existing device",
    response_model=Schedule,
    name="Create a scheduled wake-up",
    tags=["Scheduler"]
)
async def create_schedule(schedule: ScheduleRequest) -> Schedule:
    s = Schedule(**{**schedule.__dict__, "id": -1})
    schedule_db.create_new_schedule(s)
    return schedule
