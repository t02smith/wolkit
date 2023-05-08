from sqlalchemy.orm import Session
from services.schedule.err import *
from services.schedule.model import Schedule as ScheduleModel
from services.schedule.schema import ScheduleCreate


# DB Functions

def get_all_schedules(db: Session):
    return db.query(ScheduleModel).all()


def get_schedules_for_device(device_id: int, db: Session):
    return db.query(ScheduleModel).filter(ScheduleModel.device_id == device_id).all()


def create_new_schedule(device_id: int, schedule: ScheduleCreate, db: Session):
    new_schedule = ScheduleModel(
        device_id=device_id,
        weekday=schedule.weekday,
        hour=schedule.hour,
        minute=schedule.minute,
        active=True
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


def set_schedule_active(device_id: int, schedule_id: int, state: bool, db: Session):
    s: ScheduleModel = db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id, ScheduleModel.device_id == device_id).first()
    if not s:
        raise ScheduleNotFoundError(device_id, schedule_id)

    s_active = s.active == 1
    if s_active == state:
        raise ScheduleAlreadyEnabledError(device_id, schedule_id) if s_active else ScheduleAlreadyDisabledError(device_id, schedule_id)

    s.active = 1 if state else 0
    db.commit()
    db.refresh(s)


def delete_schedule(device_id: int, schedule_id: int, db: Session):
    db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id, ScheduleModel.device_id == device_id).delete()
    db.commit()
