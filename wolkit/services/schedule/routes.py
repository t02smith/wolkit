from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from auth.token import get_current_user
from auth.model import User
from db.connection import get_db
from router.responses import GenericResponse
from services.schedule import queries as schedule_db
from pydantic import BaseModel
from services.schedule.schema import ScheduleCreate, Schedule as ScheduleSchema

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
    name="Get Schedules by Device",
    response_model=List[ScheduleSchema],
    tags=["Scheduler"])
async def get_all_schedules_for_device(device_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return schedule_db.get_schedules_for_device(device_id, db)


@schedules_router.post(
    "/",
    status_code=201,
    description="Add a new schedule for an existing device",
    name="Create a scheduled wake-up",
    response_model=ScheduleSchema,
    tags=["Scheduler"]
)
async def create_schedule(device_id: int, schedule: ScheduleCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return schedule_db.create_new_schedule(device_id, schedule, db)


@schedules_router.put(
    "/{schedule_id}/disable",
    status_code=200,
    description="Disable an active schedule",
    name="Pause Schedule",
    response_model=GenericResponse,
    tags=["Scheduler"]
)
async def pause_schedule(device_id: int, schedule_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    schedule_db.set_schedule_active(device_id, schedule_id, False, db)
    return GenericResponse(message=f"Schedule {schedule_id} for device {device_id} set to enabled")


@schedules_router.put(
    "/{schedule_id}/enable",
    status_code=200,
    description="Disable an inactive schedule",
    name="Enable Schedule",
    response_model=GenericResponse,
    tags=["Scheduler"]
)
async def enable_schedule(device_id: int, schedule_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    schedule_db.set_schedule_active(device_id, schedule_id, True, db)
    return GenericResponse(message=f"Schedule {schedule_id} for device {device_id} set to disabled")


@schedules_router.delete(
    "/{schedule_id}",
    status_code=204,
    description="Delete an existing schedule",
    name="Delete Schedule",
    response_model=None,
    tags=["Scheduler"]
)
async def delete_schedule(device_id: int, schedule_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    schedule_db.delete_schedule(device_id, schedule_id, db)
