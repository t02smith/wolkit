from sqlalchemy.orm import Session

import services.wireless.queries as wat_db
import datetime
import bluetooth
import logging as log
import asyncio


async def watch_bluetooth(db: Session):
    """
    Watch for bluetooth devices available
    :return:
    """
    watchers = list(filter(lambda d: d.bluetooth, wat_db.get_all_watchers(db)))
    if len(watchers) == 0:
        log.debug("No devices to watch => terminating")
        return

    while True:
        log.debug("starting bluetooth scan")
        found_devices = set(map(
            lambda bd: bd[0],
            bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)))
        log.debug(f"found {found_devices}")

        for device in watchers:
            if device.in_timeout():
                continue

            if not any(filter(lambda d: device.mac_addr in found_devices, found_devices)):
                continue

            log.info(f"Bluetooth device {device.mac_addr} found => starting wake for {len(device.wakes)} devices")
            [d.wake() for d in device.wakes]
            device.last_checked = datetime.datetime.now()
        await asyncio.sleep(5)
