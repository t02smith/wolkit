import time
from db.connection import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class WatcherDevice(Base):
    __tablename__ = "watchers"

    id = Column(Integer, primary_key=True, index=True)

    mac_addr = Column(String, unique=True, nullable=False)
    bluetooth = Column(Boolean, nullable=False)

    ip_addr = Column(String, unique=True, nullable=False)
    lan = Column(Boolean, nullable=False)

    timeout_minutes = Column(Integer, nullable=False)
    last_checked = Column(Integer, nullable=True)

    wakes = relationship("WakeableDevice", back_populates="waked_by", secondary="watchers_mapping", lazy=True)

    def in_timeout(self) -> bool:
        if self.last_checked is None:
            return False

        timestamp = int(time.time())
        return (timestamp - self.last_checked) // 60 <= self.timeout_minutes


class WatcherDeviceMapping(Base):
    __tablename__ = "watchers_mapping"

    watcher_device_id = Column(Integer, ForeignKey("watchers.id"), primary_key=True)
    wake_device_id = Column(Integer, ForeignKey("devices.id"), primary_key=True)