from lib.device import Device
from typing import List
from pydantic import BaseModel


class Watcher(BaseModel):
    """
    We listen for this device over several mediums and if we find it then
    we wake the target device as it is specified
    """
    id: int

    """
    To scan for bluetooth we need to know the device's MAC address
    TODO
    """
    mac_addr: str
    bluetooth: bool

    """
    To scan for wireless we can do an ARP request to see if the device is
    in the network or not but we need to know its IP address.
    """
    ip_addr: str
    wireless: bool

    # the devices that we wake when this device is found
    wakes: List[Device | int | str]


