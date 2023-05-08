from sqlalchemy.orm import Session
from services.wireless.err import WatcherNotFoundError
from services.wireless.model import WatcherDevice as WatcherDeviceModel
from services.wireless.schema import WatcherDeviceCreate


# Select statements

def get_all_watchers(db: Session):
    return db.query(WatcherDeviceModel).all()


def get_watcher_by_id(watcher_id: int, db: Session):
    res = db.query(WatcherDeviceModel).filter(WatcherDeviceModel.id == watcher_id).one()
    if not res:
        raise WatcherNotFoundError(watcher_id)

    return res


# def get_wakes_by_watcher_id(watcher_id: int, db: Session):
#     return [d[0] for d in db_cursor.execute(
#         """SELECT devices.alias
#         FROM watchers_mapping
#         NATURAL JOIN devices
#         WHERE watchers_mapping.watched_device_id=?""",
#         (watcher_id,)).fetchall()]


def create_watcher(watcher: WatcherDeviceCreate, db: Session):
    new_watcher = WatcherDeviceModel(
        mac_addr=watcher.mac_addr,
        bluetooth=watcher.bluetooth,
        ip_addr=watcher.ip_addr,
        lan=watcher.lan,
        timeout_minutes=watcher.timeout_minutes
    )
    db.add(new_watcher)
    db.commit()
    db.refresh(new_watcher)
    return new_watcher
