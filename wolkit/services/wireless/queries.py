from sqlalchemy.orm import Session
from services.wireless.err import WatcherNotFoundError
from services.wireless.model import WatcherDevice as WatcherDeviceModel, WatcherDeviceMapping
from services.wireless.schema import *
from devices.model import WakeableDevice as WakeableDeviceModel
from devices.err import DeviceNotFoundError


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


def map_watcher_to_wakeable_device(watcher_id: int, wakeable_id: int, db: Session):
    watcher = db.query(WatcherDeviceModel).filter(WatcherDeviceModel.id == watcher_id).first()
    if not watcher:
        raise WatcherNotFoundError(watcher_id)

    wakeable = db.query(WakeableDeviceModel).filter(WatcherDeviceModel.id == wakeable_id).first()
    if not wakeable:
        raise DeviceNotFoundError(wakeable_id)

    new_mapping = WatcherDeviceMapping(
        watcher_device_id=watcher_id,
        wake_device_id=wakeable_id
    )
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    return new_mapping


def remove_mapping(watcher_id: int, wakeable_id: int, db: Session):
    db.query(WatcherDeviceMapping).filter(
        WatcherDeviceMapping.watcher_device_id == watcher_id,
        WatcherDeviceMapping.wake_device_id == wakeable_id
    ).delete()
    db.commit()


def remove_watcher(watcher_id: int, db: Session):
    db.query(WatcherDeviceMapping).filter(WatcherDeviceMapping.watcher_device_id == watcher_id).delete()
    db.query(WatcherDeviceModel).filter(WatcherDeviceModel.id == watcher_id).delete()


def patch_watcher(watcher_id: int, update: WatcherDevicePatch, db: Session):
    w: WatcherDeviceModel = db.query(WatcherDeviceModel).filter(WatcherDeviceModel.id == watcher_id).first()
    if not w:
        raise WatcherNotFoundError(watcher_id)

    if update.mac_addr is not None:
        w.mac_addr = update.mac_addr

    if update.bluetooth is not None:
        w.bluetooth = update.bluetooth

    if update.ip_addr is not None:
        w.ip_addr = update.ip_addr

    if update.lan is not None:
        w.lan = update.lan

    if update.timeout_minutes is not None:
        w.timeout_minutes = update.lan

    db.commit()
    db.refresh(w)
    return w


def update_watcher(watcher_id: int, update: WatcherDeviceUpdate, db: Session):
    w: WatcherDeviceModel = db.query(WatcherDeviceModel).filter(WatcherDeviceModel.id == watcher_id).first()
    if not w:
        raise WatcherNotFoundError(watcher_id)

    w.mac_addr = update.mac_addr
    w.bluetooth = update.bluetooth
    w.ip_addr = update.ip_addr
    w.lan = update.lan
    w.timeout_minutes = update.lan

    db.commit()
    db.refresh(w)
    return w