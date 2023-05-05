from db import _cursor, _connection
from lib.services import Service

services = [
    ("scheduler", "Schedules days and times each week to wake a device.", 1),
    ("sniffer", "Listens for packets being sent to a target computer and will wake the device if need be.", 0),
    ("lan_listen", "Wakes a target device based upon whether a given other device is present in the network", 0),
    ("bluetooth", "Listen for nearby bluetooth devices to trigger device wakes.", 1)
]


def create_services_table():
    _cursor.execute("""CREATE TABLE IF NOT EXISTS services (
        name TEXT PRIMARY KEY,
        description TEXT,
        active INTEGER NOT NULL
    );""")

    _cursor.executemany("""INSERT OR IGNORE INTO services VALUES (?, ?, ?)""", services)


def get_services():
    return [Service(**{
        "name": s[0],
        "description": s[1],
        "active": s[2] == 1
    }) for s in _cursor.execute("SELECT * FROM services;").fetchall()]


# def set_service(service_name: str, new_value: bool):
#