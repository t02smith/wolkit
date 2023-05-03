from pydantic import BaseModel
from net.wol import send_magic_packet


class Device(BaseModel):
    id: int
    alias: str
    mac_addr: str
    ip_addr: str

    def wake(self):
        send_magic_packet(self.mac_addr, "192.168.1.255")
