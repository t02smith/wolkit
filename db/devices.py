from db import _cursor, _connection
from typing import List
from lib.device import Device


# Utility

def _device_tuple_factory(device) -> Device:
    return Device(**{"id": device[0], "mac_addr": device[1], "alias": device[2], "ip_addr": device[3]})


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

def get_all_devices() -> List[Device]:
    """
    Returns a list of all devices recorded
    :return: list of recorded devices
    """
    return [_device_tuple_factory(d) for d in _cursor.execute("SELECT * FROM devices;").fetchall()]


def find_device_by_alias(alias: str) -> Device | None:
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

def new_device(device: Device):
    _cursor.execute(
        "INSERT INTO devices (mac_addr, alias, ip_addr) VALUES (?, ?, ?);",
        (device.mac_addr, device.alias, device.ip_addr)
    )
    _connection.commit()
