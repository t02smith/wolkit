from db.connection import db_cursor, db_con
from typing import List
from services.schedule.err import *
from services.schedule.schedule import Schedule
from devices.model import WakeableDevice


# Utility

def _schedule_factory_for_device_obj(schedule):
    return Schedule(**{
        "id": schedule[0],
        "weekday": schedule[2],
        "hour": schedule[3],
        "minute": schedule[4],
        "active": schedule[5] == 1,
        "device": WakeableDevice(**{
            "id": schedule[1],
            "mac_addr": schedule[6],
            "alias": schedule[7],
            "ip_addr": schedule[8]
        })
    })


def _schedule_factory_for_device_id(schedule):
    return Schedule(**{
        "id": schedule[0],
        "weekday": schedule[2],
        "hour": schedule[3],
        "minute": schedule[4],
        "device": schedule[1],
        "active": schedule[5] == 1
    })


# DB Functions

def create_schedules_table():
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        weekday INTEGER NOT NULL,
        hour INTEGER NOT NULL,
        minute INTEGER NOT NULL,
        active INTEGER NOT NULL,
        FOREIGN KEY (device_id) REFERENCES devices(id)
    );""")


def get_all_schedules(with_device_obj: bool = False) -> List[Schedule]:
    if with_device_obj:
        return [_schedule_factory_for_device_obj(sd) for sd in
                db_cursor.execute("SELECT * FROM schedules INNER JOIN devices")
                .fetchall()]

    return [_schedule_factory_for_device_id(sd) for sd in
            db_cursor.execute("SELECT * FROM schedules;")
            .fetchall()]


def get_schedules_for_device(device_id: int, with_device_obj: bool = False) -> List[Schedule]:
    if with_device_obj:
        return [_schedule_factory_for_device_obj(sd) for sd in
                db_cursor.execute("SELECT * FROM schedules INNER JOIN devices WHERE schedules.device_id=?;", [device_id])
                .fetchall()]

    return [_schedule_factory_for_device_id(sd) for sd in
            db_cursor.execute("SELECT * FROM schedules WHERE device_id=?;", [device_id])
            .fetchall()]


def create_new_schedule(schedule: Schedule) -> Schedule:
    db_cursor.execute("""INSERT INTO schedules 
        (device_id, weekday, hour, minute, active) VALUES
        (?, ?, ?, ?, 1);""",
        (schedule.device, schedule.weekday, schedule.hour, schedule.minute)
    )
    db_con.commit()
    return schedule


def set_schedule_active(device_id: int, schedule_id: int, state: bool):
    s = db_cursor.execute("SELECT * FROM schedules WHERE device_id=? AND id=?", (device_id, schedule_id)).fetchone()
    if s is None:
        raise ScheduleNotFoundError(device_id, schedule_id)

    s_active = s[5] == 1
    if s_active == state:
        raise ScheduleAlreadyEnabledError(device_id, schedule_id) if s_active else ScheduleAlreadyDisabledError(device_id, schedule_id)

    db_cursor.execute("UPDATE schedules SET active=? WHERE device_id=? AND id=?", (1 if state else 0, device_id, schedule_id))
    db_con.commit()

def delete_schedule(device_id: int, schedule_id: int):
    s = db_cursor.execute("SELECT * FROM schedules WHERE device_id=? AND id=?", (device_id, schedule_id)).fetchone()
    if s is None:
        raise ScheduleNotFoundError(device_id, schedule_id)

    db_cursor.execute("DELETE FROM schedules WHERE device_id=? AND id=?", (device_id, schedule_id))
    db_con.commit()
