from db import _cursor, _connection
from lib.watchers import WatcherDevice
from db.devices import _device_tuple_factory


#

def _watcher_tuple_factory(w) -> WatcherDevice:
    return WatcherDevice(**{
        "id": w[0],
        "mac_addr": w[1],
        "bluetooth": w[3] == 1,
        "ip_addr": w[2],
        "wireless": [4] == 1,
        "wakes": get_wakes_by_watcher_id(w[0]),
        "timeout_minutes": w[5]
    })


#

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
        wireless INTEGER NOT NULL,
        timeout INTEGER NOT NULL
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
        watcher_devices.append(WatcherDevice(**{
            "id": wd[0],
            "mac_addr": wd[1],
            "ip_addr": wd[2],
            "bluetooth": wd[3] == 1,
            "wireless": wd[4] == 1,
            "timeout_minutes": wd[5],
            "wakes": [_device_tuple_factory(d) for d in _cursor.execute("""
            SELECT * from devices 
            WHERE id in (
                SELECT wake_device_id 
                FROM watchers_mapping
                WHERE watched_device_id=?
            );""", (wd[0],)).fetchall()]
        }))
    return watcher_devices


def get_watcher_by_id(watcher_id: int):
    wd = _cursor.execute("SELECT * FROM watchers WHERE id=?", (watcher_id,)).fetchone()
    if wd is None:
        return None

    return _watcher_tuple_factory(wd)


def get_wakes_by_watcher_id(watcher_id: int):
    return [d[0] for d in _cursor.execute(
        """SELECT devices.alias 
        FROM watchers_mapping 
        NATURAL JOIN devices 
        WHERE watchers_mapping.watched_device_id=?""",
        (watcher_id,)).fetchall()]


def create_watcher(watcher: WatcherDevice) -> WatcherDevice:
    _cursor.execute("""
        INSERT INTO watchers (mac_addr, ip_addr, bluetooth, wireless, timeout)
        VALUES (?, ?, ?, ?, ?)
        """, (watcher.mac_addr, watcher.ip_addr, 1 if watcher.bluetooth else 0, 1 if watcher.wireless else 0,
              watcher.timeout_minutes))
    _connection.commit()
    return watcher
