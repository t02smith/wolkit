from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Session
from db.connection import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("WakeableDevice", back_populates="schedules", lazy=True)

    weekday = Column(Integer, nullable=False, index=False)
    hour = Column(Integer, nullable=False, index=False)
    minute = Column(Integer, nullable=False, index=False)
    active = Column(Boolean, nullable=False, index=False)

