from pydantic import BaseModel
from wolkit.net.wol import send_magic_packet
from scapy.layers.inet import *
from enum import Enum
from datetime import datetime


class WakeableDeviceStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1
    UNKNOWN = 2


class WakeableDevice(BaseModel):
    """
    Represents a device that can be woken up over the network
    """
    id: int

    # a nickname to make it more easily recognisable
    alias: str

    # unique address for the device
    mac_addr: str

    # static ip address for the device
    ip_addr: str

    # whether the device is currently active
    status: WakeableDeviceStatus = WakeableDeviceStatus.UNKNOWN

    def wake(self) -> None:
        """
        Wake a device up from sleep if it is not already awake
        :return: None
        """
        if self.status == WakeableDeviceStatus.UNKNOWN:
            self.status = WakeableDeviceStatus.ACTIVE if is_active(self.ip_addr) else WakeableDeviceStatus.INACTIVE

        if self.status == WakeableDeviceStatus.ACTIVE:
            return

        send_magic_packet(self.mac_addr, "192.168.1.255")
        self.status = WakeableDeviceStatus.ACTIVE


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
