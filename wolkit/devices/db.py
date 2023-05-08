import sqlite3

from db.connection import db_cursor, db_con
from typing import List, Union
from devices.device import WakeableDevice
import devices.err as err_dev

# Utility

def device_tuple_factory(device) -> WakeableDevice:
    return WakeableDevice(**{"id": device[0], "mac_addr": device[1], "alias": device[2], "ip_addr": device[3]})


# DB functions

def create_devices_table() -> None:
    """
    Create a new devices tables
    :return: None
    """
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS devices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac_addr TEXT NOT NULL UNIQUE,
            alias TEXT NOT NULL UNIQUE,
            ip_addr TEXT
        );""")


# Select statements

def get_all_devices() -> List[WakeableDevice]:
    """
    Returns a list of all devices recorded
    :return: list of recorded devices
    """
    return [device_tuple_factory(d) for d in db_cursor.execute("SELECT * FROM devices;").fetchall()]


def get_device_by_id(device_id: int) -> WakeableDevice:
    res = db_cursor.execute("SELECT * FROM devices WHERE id=?", [device_id]).fetchone()
    if res is None:
        raise err_dev.DeviceNotFoundError(device_id)

    return device_tuple_factory(res)


# Insert statements

def new_device(device: WakeableDevice) -> WakeableDevice:
    try :
        db_cursor.execute(
            "INSERT INTO devices (mac_addr, alias, ip_addr) VALUES (?, ?, ?);",
            (device.mac_addr.upper(), device.alias, device.ip_addr)
        )
        db_con.commit()
        return device_tuple_factory(db_cursor.execute("SELECT * FROM devices WHERE id=?", (db_cursor.lastrowid,)).fetchone())
    except sqlite3.IntegrityError as e:
        raise err_dev.DeviceDetailsAlreadyUsed(e.args[0])


def delete_device(device_id: int):
    db_cursor.execute("DELETE FROM watchers_mapping WHERE wake_device_id=?", [device_id])
    db_cursor.execute("DELETE FROM schedules WHERE device_id=?", [device_id])
    db_cursor.execute("DELETE FROM devices WHERE id=?", [device_id])
    db_con.commit()
