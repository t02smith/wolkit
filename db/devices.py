import sqlite3

from db import _cursor, _connection
from typing import List, Union
from lib.devices import WakeableDevice
import errors.devices as err_dev

# Utility

def _device_tuple_factory(device) -> WakeableDevice:
    return WakeableDevice(**{"id": device[0], "mac_addr": device[1], "alias": device[2], "ip_addr": device[3]})


# DB functions

def create_devices_table() -> None:
    """
    Create a new devices tables
    :return: None
    """
    _cursor.execute("""CREATE TABLE IF NOT EXISTS devices(
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
    return [_device_tuple_factory(d) for d in _cursor.execute("SELECT * FROM devices;").fetchall()]


def find_device_by_alias(alias: str) -> Union[WakeableDevice, None]:
    """
    Find a device by its alias and return it
    :param alias: the alias to search for
    :return: the device if it exists or none
    """
    result = _cursor.execute(
        "SELECT * FROM devices WHERE alias=?;",
        [alias]
    ).fetchone()

    if len(result) == 0:
        return None

    return _device_tuple_factory(result)


# Insert statements

def new_device(device: WakeableDevice) -> WakeableDevice:
    try :
        _cursor.execute(
            "INSERT INTO devices (mac_addr, alias, ip_addr) VALUES (?, ?, ?);",
            (device.mac_addr.upper(), device.alias, device.ip_addr)
        )
    except sqlite3.IntegrityError as e:
        raise err_dev.DeviceDetailsAlreadyUsed(e.args[0])

    _connection.commit()

    return _device_tuple_factory(_cursor.execute("SELECT * FROM devices WHERE id=?", (_cursor.lastrowid, )).fetchone())
