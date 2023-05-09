import time
from db.connection import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class WatcherDevice(Base):
    __tablename__ = "watchers"

    id = Column(Integer, primary_key=True, index=True)

    bluetooth_mac_addr = Column(String, unique=True, nullable=False)
    lan_ip_addr = Column(String, unique=True, nullable=False)

    timeout_minutes = Column(Integer, nullable=False)
    last_checked = Column(Integer, default=-1, nullable=False)

    watcher_mappings = relationship("WatcherDeviceMapping", back_populates="watches")

    def in_timeout(self) -> bool:
        if self.last_checked == -1:
            return False

        timestamp = int(time.time())
        return (timestamp - self.last_checked) // 60 <= self.timeout_minutes


class WatcherDeviceMapping(Base):
    __tablename__ = "watcher_device_mapping"

    watcher_device_id = Column(Integer, ForeignKey("watchers.id"), primary_key=True)
    watches = relationship("WatcherDevice", back_populates="watcher_mappings")

    wake_device_id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    wakes = relationship("WakeableDevice", back_populates="woken_by_mappings")

    bluetooth = Column(Boolean, nullable=False)
    lan = Column(Boolean, nullable=False)
    sniff_traffic = Column(Boolean, nullable=False)
