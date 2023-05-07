from scapy.all import *
import db.devices as dev_db
import logging as log


async def listen_for_packets(host_ip_addr: str) -> None:
    """
    Listen for incoming packets to registered devices and wake them if any appear
    :param host_ip_addr: the local ip address of this machine
    :return: None
    """
    log.info("starting device listener")
    devices = dev_db.get_all_devices()
    if len(devices) == 0:
        log.debug("No tracked devices => listen not started")
        return

    for d in devices:
        sniffer = AsyncSniffer(
            filter=f"icmp and dst host {d.ip_addr} and not src {host_ip_addr}",
            prn=lambda p: packet_callback(p, d),
            store=False)
        sniffer.start()

    log.info("Started packet listeners")


def packet_callback(pkt, device) -> None:
    """
    Called every time a valid packet is received
    :param pkt: the packet received
    :param device: the device that this packet was sent to
    """
    device.wake()



