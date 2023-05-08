import sqlite3
from sqlalchemy.orm import Session
from db.connection import db_cursor, db_con, get_db
from typing import List, Union
from devices.model import WakeableDevice as WakeableDeviceModel
from devices.schema import WakeableDevice, WakeableDeviceCreate
import devices.err as err_dev
from fastapi import Depends


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
    d = db.query(WakeableDeviceModel).filter(WakeableDeviceModel.id == device_id).first()
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
        mac_addr=device.mac_addr,
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
    db.query(WakeableDeviceModel).filter(WakeableDeviceModel.id == device_id).delete()

    db.commit()

    # db_cursor.execute("DELETE FROM watchers_mapping WHERE wake_device_id=?", [device_id])
    # db_cursor.execute("DELETE FROM schedules WHERE device_id=?", [device_id])
    # db_cursor.execute("DELETE FROM devices WHERE id=?", [device_id])
    # db_con.commit()
