from scapy.all import *
from sqlalchemy.orm import Session
from typing import List
from services.wireless.model import WatcherDeviceMapping
from services.wireless.queries import get_sniff_traffic_mappings


async def listen_for_packets(db: Session) -> None:
    """
    Listen for incoming packets to registered devices and wake them if any appear
    :return: None
    """
    print("enabling service packet listener")
    mappings = get_sniff_traffic_mappings(db)

    if len(mappings) == 0:
        print("No tracked devices => listen not started")
        return

    for mapping in mappings:
        sniffer = AsyncSniffer(
            filter=f"dst host {mapping.watches.lan_ip_addr} and not arp",
            prn=lambda p: packet_callback(p, mapping.watches, mapping.wakes, db),
            store=False)
        sniffer.start()

    print("Started packet listeners")


def packet_callback(pkt, watcher, device, db) -> None:
    """
    Called every time a valid packet is received
    :param pkt: the packet received
    :param watcher
    :param device: the device that this packet was sent to
    """
    if watcher.in_timeout():
        return

    print(f"waking {device.alias}")
    device.wake()
    watcher.last_checked = int(time.time())
    db.commit()



