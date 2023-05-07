import time
import datetime
from pydantic import BaseModel
from lib.devices import WakeableDevice
import db.schedule as schedule_db
import asyncio
import logging as log
from typing import Union


class Schedule(BaseModel):
    id: int
    device: Union[WakeableDevice, int]
    weekday: int
    hour: int
    minute: int


# schedule listener

async def schedule_watcher():
    log.info("Scheduler started")
    while True:
        timestamp = datetime.datetime.now()
        schedules = schedule_db.get_all_schedules(True)
        weekday, hour, minute = timestamp.weekday(), timestamp.hour, timestamp.minute
        for s in schedules:
            if s.weekday == weekday and s.hour == hour and s.minute == minute:
                log.info(f"SCHEDULER: Waking device {s.device.alias}")
                s.device.wake()

        await asyncio.sleep(60)
