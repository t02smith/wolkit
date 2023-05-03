from db import _cursor, _connection
from typing import List
from lib.device import Device


# Utility

def _device_tuple_factory(device) -> Device:
    return Device(**{"id": device[0], "mac_addr": device[1], "alias": device[2], "ip_addr": device[3]})


# DB functions

def create_devices_table():
    _cursor.execute("""CREATE TABLE IF NOT EXISTS devices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac_addr TEXT NOT NULL UNIQUE,
            alias TEXT NOT NULL UNIQUE,
            ip_addr TEXT
        );""")


def get_all_devices() -> List[Device]:
    return [_device_tuple_factory(d) for d in _cursor.execute("SELECT * FROM devices;").fetchall()]


def new_device(device: Device):
    _cursor.execute(
        "INSERT INTO devices (mac_addr, alias, ip_addr) VALUES (?, ?, ?);",
        (device.mac_addr, device.alias, device.ip_addr)
    )
    _connection.commit()


def find_device_by_alias(alias: str) -> Device | None:
    result = _cursor.execute(
        "SELECT * FROM devices WHERE alias=?;",
        [alias]
    ).fetchone()

    if len(result) == 0:
        return None

    return _device_tuple_factory(result)