import sqlite3
from sqlalchemy.orm import Session
from db.connection import get_db
from typing import List, Union
from devices.model import WakeableDevice as WakeableDeviceModel
from devices.schema import *
import devices.err as err_dev
from fastapi import Depends
from services.schedule.model import Schedule
from services.wireless.model import WatcherDeviceMapping


# Select statements

def get_all_devices(db: Session):
    """
    Returns a list of all devices recorded
    :return: list of recorded devices
    """
    return db.query(WakeableDeviceModel).all()


def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    """
    Get a wakeable device using its ID from the DB
    """
    d = db.query(WakeableDeviceModel).filter_by(id=device_id).first()
    if not d:
        raise err_dev.DeviceNotFoundError(device_id)

    return d


# Insert statements

def new_device(device: WakeableDeviceCreate, db: Session):
    """
    Create a new device and insert it into the database
    If the alias or mac address has already been used then it will throw
    an exception
    """
    d = WakeableDeviceModel(
        alias=device.alias,
        mac_addr=device.mac_addr.upper(),
        ip_addr=device.ip_addr
    )
    db.add(d)
    db.commit()
    db.refresh(d)

    return d


def delete_device(device_id: int, db: Session):
    """
    Delete a device from the database.
    This will include any records from the watchers or scheduling tables that reference it
    """
    db.query(Schedule).filter_by(device_id=device_id).delete()
    db.query(WatcherDeviceMapping).filter_by(wake_device_id=device_id).delete()
    db.query(WakeableDeviceModel).filter(id=device_id).delete()

    db.commit()


def patch_device(device_id: int, update: WakeableDevicePatch, db: Session):
    d = db.query(WakeableDeviceModel).filter_by(id=device_id).first()
    if not d:
        raise err_dev.DeviceNotFoundError(device_id)

    if update.alias is not None:
        d.alias = update.alias

    if update.ip_addr is not None:
        d.ip_addr = update.ip_addr

    if update.mac_addr is not None:
        d.mac_addr = update.mac_addr

    db.commit()
    db.refresh(d)
    return d


def update_device(device_id: int, update: WakeableDevicePatch, db: Session):
    d = db.query(WakeableDeviceModel).filter_by(id=device_id).first()
    if not d:
        raise err_dev.DeviceNotFoundError(device_id)

    d.alias = update.alias
    d.ip_addr = update.ip_addr
    d.mac_addr = update.mac_addr

    db.commit()
    db.refresh(d)
    return d
