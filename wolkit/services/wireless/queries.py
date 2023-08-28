from sqlalchemy.orm import Session
from services.wireless.err import WatcherNotFoundError
from services.wireless.model import WatcherDevice as WatcherDeviceModel, WatcherDeviceMapping as WatcherDeviceMappingModel
from services.wireless.schema import *
from devices.model import WakeableDevice as WakeableDeviceModel
from devices.err import DeviceNotFoundError


# Select statements

def get_all_watchers(db: Session):
    return db.query(WatcherDeviceModel).all()


def get_watcher_by_id(watcher_id: int, db: Session):
    res = db.query(WatcherDeviceModel).filter_by(id=watcher_id).one()
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
        bluetooth_mac_addr=watcher.bluetooth_mac_addr.lower(),
        lan_ip_addr=watcher.lan_ip_addr,
        timeout_minutes=watcher.timeout_minutes
    )
    db.add(new_watcher)
    db.commit()
    db.refresh(new_watcher)
    return new_watcher


def map_watcher_to_wakeable_device(watcher_id: int, wakeable_id: int, mapping: WatcherDeviceMappingCreate, db: Session):
    watcher = db.query(WatcherDeviceModel).filter_by(id=watcher_id).first()
    if not watcher:
        raise WatcherNotFoundError(watcher_id)

    wakeable = db.query(WakeableDeviceModel).filter_by(id=wakeable_id).first()
    if not wakeable:
        raise DeviceNotFoundError(wakeable_id)

    new_mapping = WatcherDeviceMappingModel(
        watcher_device_id=watcher_id,
        wake_device_id=wakeable_id,
        lan=mapping.lan,
        bluetooth=mapping.bluetooth,
        sniff_traffic=mapping.sniff_traffic
    )
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    return new_mapping


def remove_mapping(watcher_id: int, wakeable_id: int, db: Session):
    db.query(WatcherDeviceMappingModel).filter(
        WatcherDeviceMappingModel.watcher_device_id == watcher_id,
        WatcherDeviceMappingModel.wake_device_id == wakeable_id
    ).delete()
    db.commit()


def remove_watcher(watcher_id: int, db: Session):
    db.query(WatcherDeviceMappingModel).filter_by(watcher_device_id=watcher_id).delete()
    db.query(WatcherDeviceModel).filter_by(id=watcher_id).delete()


def patch_watcher(watcher_id: int, update: WatcherDevicePatch, db: Session):
    w = db.query(WatcherDeviceModel).filter_by(id=watcher_id).first()
    if not w:
        raise WatcherNotFoundError(watcher_id)

    if update.bluetooth_mac_addr is not None:
        w.mac_addr = update.bluetooth_mac_addr.lower()

    if update.lan_ip_addr is not None:
        w.ip_addr = update.lan_ip_addr

    if update.timeout_minutes is not None:
        w.timeout_minutes = update.timeout_minutes

    db.commit()
    db.refresh(w)
    return w


def update_watcher(watcher_id: int, update: WatcherDeviceUpdate, db: Session):
    w = db.query(WatcherDeviceModel).filter_by(id=watcher_id).first()
    if not w:
        raise WatcherNotFoundError(watcher_id)

    w.bluetooth_mac_addr = update.bluetooth_mac_addr.lower()
    w.lan_ip_addr = update.lan_ip_addr
    w.timeout_minutes = update.timeout_minutes

    db.commit()
    db.refresh(w)
    return w


def get_bluetooth_mappings(db: Session):
    return db.query(WatcherDeviceMappingModel).filter_by(bluetooth=True).all()


def get_lan_mappings(db: Session):
    return db.query(WatcherDeviceMappingModel).filter_by(lan=True).all()


def get_sniff_traffic_mappings(db: Session):
    return db.query(WatcherDeviceMappingModel).filter_by(sniff_traffic=True).all()
