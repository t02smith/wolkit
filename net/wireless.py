import time
from lib.device import is_active
import db.watchers as wat_db
import logging as log

async def watch_LAN():
    """
    Watch the LAN for registered devices appearing\
    :return:
    """
    watchers = list(filter(lambda d: d.wireless, wat_db.get_all_watchers()))
    if len(watchers) == 0:
        log.info("No devices to watch => terminating")
        return

    while True:
        for device in watchers:
            if not is_active(device.ip_addr):
                continue

            print(f"Device found => starting wake for {len(device.wakes)} devices")
            [d.wake() for d in device.wakes]
        time.sleep(5)