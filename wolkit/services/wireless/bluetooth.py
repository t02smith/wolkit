import time

from sqlalchemy.orm import Session
import services.wireless.queries as wat_db
import datetime
import bluetooth
import asyncio


async def watch_bluetooth(db: Session):
    """
    Watch for bluetooth devices available
    :return:
    """
    print("enabled service bluetooth listener")
    mappings = wat_db.get_bluetooth_mappings(db)
    if len(mappings) == 0:
        print("No devices to watch => terminating")
        return

    while True:
        print("starting bluetooth scan")
        found_devices = set(map(
            lambda bd: bd[0],
            bluetooth.discover_devices(duration=4, lookup_names=True, flush_cache=True, lookup_class=False)))
        print(f"found bluetooth devices {found_devices}")

        for mapping in mappings:
            if mapping.watches.in_timeout():
                continue

            if not any(filter(lambda d: mapping.watches.bluetooth_mac_addr in found_devices, found_devices)):
                continue

            print(f"Bluetooth device {mapping.watches.bluetooth_mac_addr} found => starting wake for {mapping.wakes.mac_addr}")
            mapping.wakes.wake()
            mapping.wakes.last_checked = int(time.time())
        db.commit()
        await asyncio.sleep(10)
