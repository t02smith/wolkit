import datetime
from services.schedule import queries as schedule_db
import asyncio
import logging as log
from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Session
from db.connection import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("WakeableDevice", back_populates="schedules")

    weekday = Column(Integer, nullable=False, index=False)
    hour = Column(Integer, nullable=False, index=False)
    minute = Column(Integer, nullable=False, index=False)
    active = Column(Boolean, nullable=False, index=False)


# schedule listener

async def schedule_service(db: Session):
    log.info("Scheduler started")
    while True:
        timestamp = datetime.datetime.now()
        schedules = schedule_db.get_all_schedules(db)
        weekday, hour, minute = timestamp.weekday(), timestamp.hour, timestamp.minute
        for s in schedules:
            if s.weekday == weekday and s.hour == hour and s.minute == minute:
                log.info(f"SCHEDULER: Waking device {s.device.alias}")
                s.device.wake()

        await asyncio.sleep(60)
