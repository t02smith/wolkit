from pydantic import BaseModel
from net.wol import send_magic_packet
from scapy.layers.inet import *
from enum import Enum


class DeviceStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1
    UNKNOWN = 2


class Device(BaseModel):
    id: int
    alias: str
    mac_addr: str
    ip_addr: str
    status: DeviceStatus = DeviceStatus.UNKNOWN

    def wake(self):
        if self.status == DeviceStatus.UNKNOWN:
            self.status = DeviceStatus.ACTIVE if is_active(self.ip_addr) else DeviceStatus.INACTIVE

        if self.status == DeviceStatus.ACTIVE:
            return

        send_magic_packet(self.mac_addr, "192.168.1.255")
        self.status = DeviceStatus.ACTIVE


def is_active(ip_addr: str) -> bool:
    """
    Sends an ARP request to check if a device is active
    :param ip_addr: the target device's ip address
    :return: device is active or not
    """
    icmp_req = IP(dst=ip_addr) / ICMP()
    res = sr1(icmp_req, timeout=1, verbose=False)

    return res is not None \
        and res.haslayer(ICMP) \
        and res[ICMP].type == 0
