import datetime

from sqlalchemy.orm import Session

from devices.model import is_active
import services.wireless.queries as wat_db
import logging as log
import asyncio


async def watch_LAN(db: Session):
    """
    Watch the LAN for registered devices appearing
    :return: None
    """
    watchers = list(filter(lambda d: d.wireless, wat_db.get_all_watchers(db)))
    if len(watchers) == 0:
        log.debug("No devices to watch => terminating")
        return

    while True:
        log.debug("scanning for local wireless devices")
        for device in watchers:
            if device.in_timeout():
                continue

            if not is_active(device.ip_addr):
                continue

            log.debug(f"Device {device.ip_addr} found => starting wake for {len(device.wakes)} devices")
            [d.wake() for d in device.wakes]
            device.last_checked = datetime.datetime.now()
        await asyncio.sleep(5)
