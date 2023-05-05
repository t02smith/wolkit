from pydantic import BaseModel
import logging as log
from lib.schedule import schedule_watcher
from net.sniffer import listen_for_packets
from net.wireless import watch_LAN
from net.bluetooth import watch_bluetooth
import asyncio


class Service(BaseModel):
    """
    A service is a background task that will allow us to wake a device based
    upon a given condition.
    """
    name: str
    description: str
    active: bool


running_services = {}
services = {
    "scheduler": ("Schedules days and times each week to wake a device.", 1, schedule_watcher),
    "sniffer": ("Listens for packets being sent to a target computer and will wake the device if need be.", 0, listen_for_packets),
    "lan": ("Wakes a target device based upon whether a given other device is present in the network", 0, watch_LAN),
    "bluetooth": ("Listen for nearby bluetooth devices to trigger device wakes.", 1, watch_bluetooth)
}

def enable_all_services():
    for s in services:
        if s not in running_services:
            continue

        enable_service(s)


def disable_all_services():
    for s in services:
        if s in running_services:
            continue

        disable_service(s)


def enable_service(service_name: str) -> None:
    """
    Enable a service that is currently disabled
    :param service_name: the name of the service
    :return: None
    """
    if service_name not in services:
        log.warning("service not found")
        return

    if service_name in running_services:
        log.warning("service already running")
        return

    log.info(f"enabling service {service_name}")
    running_services[service_name] = asyncio.get_event_loop().create_task(services[service_name][2]())


def disable_service(service_name: str) -> None:
    """
    Disable a service that is currently enabled
    :param service_name: the name of the service
    :return: None
    """
    if service_name not in services:
        log.warning("service not found")
        return

    if service_name not in running_services:
        log.warning("service not running")
        return

    log.info(f"disabling service {service_name}")
    task = running_services[service_name]
    task.cancel()
    del (running_services[service_name])

