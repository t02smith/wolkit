import datetime

from sqlalchemy.orm import Session

from devices.model import is_active
import services.wireless.queries as wat_db
import asyncio


async def watch_LAN(db: Session):
    """
    Watch the LAN for registered devices appearing
    :return: None
    """
    print("enabling service LAN listener")
    mappings = wat_db.get_lan_mappings(db)
    if len(mappings) == 0:
        print("No devices to watch => terminating")
        return

    while True:
        print("scanning for local wireless devices")
        for mapping in mappings:
            if mapping.watches.in_timeout():
                continue

            if not is_active(mapping.watches.lan_ip_addr):
                continue

            print(f"Device {mapping.watches.lan_ip_addr} found => starting wake for {len(mapping.wakes.mac_addr)} devices")
            mapping.wakes.wake()
            mapping.watches.last_checked = datetime.datetime.now()
        await asyncio.sleep(5)
