from db import _cursor, _connection
from typing import List
from lib.schedule import Schedule
from lib.devices import WakeableDevice


# Utility

def _schedule_factory_for_device_obj(schedule):
    return Schedule(**{
        "id": schedule[0],
        "weekday": schedule[2],
        "hour": schedule[3],
        "minute": schedule[4],
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
        "device": schedule[1]
    })


# DB Functions

def create_schedules_table():
    _cursor.execute("""CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        weekday INTEGER NOT NULL,
        hour INTEGER NOT NULL,
        minute INTEGER NOT NULL,
        FOREIGN KEY (device_id) REFERENCES devices(id)
    );""")


def get_all_schedules(with_device_obj: bool = False) -> List[Schedule]:
    if with_device_obj:
        return [_schedule_factory_for_device_obj(sd) for sd in
                _cursor.execute("SELECT * FROM schedules INNER JOIN devices;")
                .fetchall()]

    return [_schedule_factory_for_device_id(sd) for sd in
            _cursor.execute("SELECT * FROM schedules;")
            .fetchall()]


def get_schedules_for_device(device_id: int, with_device_obj: bool = False) -> List[Schedule]:
    if with_device_obj:
        return [_schedule_factory_for_device_obj(sd) for sd in
                _cursor.execute("SELECT * FROM schedules INNER JOIN devices WHERE schedules.device_id=?;", [device_id])
                .fetchall()]

    return [_schedule_factory_for_device_id(sd) for sd in
            _cursor.execute("SELECT * FROM schedules WHERE device_id=?;", [device_id])
            .fetchall()]


def create_new_schedule(schedule: Schedule) -> Schedule:
    _cursor.execute("""INSERT INTO schedules 
        (device_id, weekday, hour, minute) VALUES
        (?, ?, ?, ?);""",
                    (schedule.device, schedule.weekday, schedule.hour, schedule.minute)
                    )
    _connection.commit()
    return schedule
