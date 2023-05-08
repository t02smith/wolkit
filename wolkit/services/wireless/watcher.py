from devices.device import WakeableDevice
from typing import List, Union
import datetime
from pydantic import BaseModel


class WatcherDevice(BaseModel):
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
    wakes: List[Union[WakeableDevice, int, str]]

    """
    Once the devices have been woken up, they won't need to be re-awoken straight
    away. By adding a timeout, we stop searching for this watcher device for a given
    amount of time
    """
    timeout_minutes: int
    last_checked: Union[datetime.datetime, None] = None

    def in_timeout(self) -> bool:
        if self.last_checked is None:
            return False

        timestamp = datetime.datetime.now()
        return (timestamp - self.last_checked).total_seconds() // 60 <= self.timeout_minutes


