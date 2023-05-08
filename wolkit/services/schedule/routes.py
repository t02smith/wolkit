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
async def create_schedule(device_id: int, schedule: ScheduleRequest, user: User = Depends(get_current_user)) -> Schedule:
    s = Schedule(**{**schedule.__dict__, "id": -1, "device": device_id, "active": True})
    schedule_db.create_new_schedule(s)
    return s


@schedules_router.put(
    "/{schedule_id}/disable",
    status_code=200,
    description="Disable an active schedule",
    name="Pause Schedule",
    tags=["Scheduler"]
)
async def pause_schedule(device_id: int, schedule_id: int, user: User = Depends(get_current_user)):
    schedule_db.set_schedule_active(device_id, schedule_id, False)
    return {"message": f"Schedule {schedule_id} for device {device_id} set to enabled"}


@schedules_router.put(
    "/{schedule_id}/enable",
    status_code=200,
    description="Disable an inactive schedule",
    name="Enable Schedule",
    tags=["Scheduler"]
)
async def enable_schedule(device_id: int, schedule_id: int, user: User = Depends(get_current_user)):
    schedule_db.set_schedule_active(device_id, schedule_id, True)
    return {"message": f"Schedule {schedule_id} for device {device_id} set to disabled"}


@schedules_router.delete(
    "/{schedule_id}",
    status_code=204,
    description="Delete an existing schedule",
    name="Delete Schedule",
    tags=["Scheduler"]
)
async def delete_schedule(device_id: int, schedule_id: int, user: User = Depends(get_current_user)):
    schedule_db.delete_schedule(device_id, schedule_id)