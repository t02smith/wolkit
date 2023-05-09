from net.wol import send_magic_packet
from scapy.layers.inet import *
from enum import Enum
from db.connection import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class WakeableDeviceStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1
    UNKNOWN = 2


class WakeableDevice(Base):
    """
    Represents a device that can be woken up over the network
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    # a nickname to make it more easily recognisable
    alias = Column(String, unique=True, index=False)

    # unique address for the device
    mac_addr = Column(String, unique=True, index=True)

    # static ip address for the device
    ip_addr = Column(String, unique=True, index=False)

    status = Column(Integer, nullable=False, default=2)

    #
    schedules = relationship("Schedule", back_populates="device", lazy=True)
    woken_by_mappings = relationship("WatcherDeviceMapping", back_populates="wakes")

    def wake(self) -> None:
        """
        Wake a device up from sleep if it is not already awake
        :return: None
        """
        if self.status == WakeableDeviceStatus.UNKNOWN.value:
            self.status = WakeableDeviceStatus.ACTIVE.value if is_active(self.ip_addr) else WakeableDeviceStatus.INACTIVE.value

        if self.status == WakeableDeviceStatus.ACTIVE.value:
            print(f"Device {self.mac_addr} already awake => terminating")
            return

        send_magic_packet(self.mac_addr, "192.168.1.255")
        self.status = WakeableDeviceStatus.ACTIVE.value


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
