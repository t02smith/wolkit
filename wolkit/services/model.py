from sqlalchemy.orm import Session, sessionmaker
from services.schedule.service import schedule_service
from services.wireless.sniffer import listen_for_packets
from services.wireless.lan import watch_LAN
from services.wireless.bluetooth import watch_bluetooth
import asyncio
from db.connection import Base, SessionLocal
from sqlalchemy import Column, Integer, String, event, Boolean


class Service(Base):
    """
    A service is a background task that will allow us to wake a device based
    upon a given condition.
    """
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)


running_services = {}
services = {
    "scheduler": {
        "obj": Service(name="scheduler", description="Schedules days and times each week to wake a device.", active=1),
        "method": schedule_service},
    "sniffer": {"obj": Service(name="sniffer",
                               description="Listens for packets being sent to a target computer and will wake the "
                                           "device if need be.",
                               active=0), "method": listen_for_packets},
    "lan": {"obj": Service(name="lan",
                           description="Listens for packets being sent to a target computer and will wake the device "
                                       "if need be.",
                           active=0), "method": watch_LAN},
    "bluetooth": {
        "obj": Service(name="bluetooth", description="Listen for nearby bluetooth devices to trigger device wakes.",
                       active=1), "method": watch_bluetooth},
}


def insert_default_service_records(target, connection, **kwargs):
    ses = sessionmaker(bind=connection)
    db = ses()

    for s, data in services.items():
        db.add(data["obj"])
    db.commit()


event.listen(Service.__table__, "after_create", insert_default_service_records)


def start_services():
    """
    Starts any services that are pitched to run on application startup
    """
    db = SessionLocal()

    s_ls = db.query(Service).filter_by(active=True).all()
    for s in s_ls:
        enable_service(s.name, db)


def enable_all_services(db: Session):
    for s in services:
        if s not in running_services:
            continue

        enable_service(s, db)


def disable_all_services():
    for s in services:
        if s in running_services:
            continue

        disable_service(s)


def enable_service(service_name: str, db: Session) -> None:
    """
    Enable a service that is currently disabled
    :param service_name: the name of the service
    :return: None
    """
    if service_name not in services:
        print("service not found")
        return

    if service_name in running_services:
        print("service already running")
        return

    print(f"enabling service {service_name}")
    running_services[service_name] = asyncio.get_event_loop().create_task(services[service_name]["method"](db))


def disable_service(service_name: str) -> None:
    """
    Disable a service that is currently enabled
    :param service_name: the name of the service
    :return: None
    """
    if service_name not in services:
        print("service not found")
        return

    if service_name not in running_services:
        print("service not running")
        return

    print(f"disabling service {service_name}")
    task = running_services[service_name]
    task.cancel()
    del (running_services[service_name])
