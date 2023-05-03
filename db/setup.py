from db.devices import create_devices_table
from db.schedule import create_schedules_table
from db import _connection
import logging as log


def setup_db():
    log.info("setting up db")
    create_devices_table()
    create_schedules_table()
    log.info("db set up successfully")
    _connection.commit()
