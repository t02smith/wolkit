from datetime import datetime
from services.schedule.queries import get_all_schedules
from sqlalchemy.orm import Session
import asyncio


async def schedule_service(db: Session):
    print("enabling service scheduler")
    while True:
        timestamp = datetime.now()
        schedules = get_all_schedules(db)
        weekday, hour, minute = timestamp.weekday(), timestamp.hour, timestamp.minute
        for s in schedules:
            if s.weekday == weekday and s.hour == hour and s.minute == minute:
                print(f"SCHEDULER: Waking device {s.device.alias}")
                s.device.wake()

        await asyncio.sleep(60)
