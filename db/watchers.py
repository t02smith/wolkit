from db import _cursor, _connection
from lib.watchers import Watcher
from db.devices import _device_tuple_factory


def create_watchers_table() -> None:
    """
    Creates a new table to for devices that we listen for
    :return: None
    """
    _cursor.execute("""CREATE TABLE IF NOT EXISTS watchers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mac_addr TEXT UNIQUE,
        ip_addr TEXT UNIQUE,
        bluetooth INTEGER NOT NULL,
        wireless INTEGER NOT NULL
    );""")


def create_watchers_mapping_table() -> None:
    """
    Creates a table that maps watcher devices to what they can wake up
    :return: None
    """
    _cursor.execute("""CREATE TABLE IF NOT EXISTS watchers_mapping (
        watched_device_id INTEGER NOT NULL,
        wake_device_id INTEGER NOT NULL,
        FOREIGN KEY (watched_device_id) REFERENCES watchers(id),
        FOREIGN KEY (wake_device_id) REFERENCES devices(id),
        PRIMARY KEY (watched_device_id, wake_device_id)
    );""")


# Select statements

def get_all_watchers():
    # get watcher devices
    wds = _cursor.execute("SELECT * FROM watchers;").fetchall()
    watcher_devices = []
    for wd in wds:
        watcher_devices.append(Watcher(**{
            "id": wd[0],
            "mac_addr": wd[1],
            "ip_addr": wd[2],
            "bluetooth": True if wd[3] == 1 else False,
            "wireless": True if wd[4] == 1 else False,
            "wakes": [_device_tuple_factory(d) for d in _cursor.execute("""
            SELECT * from devices 
            WHERE id in (
                SELECT wake_device_id 
                FROM watchers_mapping
                WHERE watched_device_id=?
            );""", (wd[0], )).fetchall()]
        }))
    return watcher_devices
