from devices.db import create_devices_table
from services.schedule.db import create_schedules_table
from services.wireless.db import create_watchers_table, create_watchers_mapping_table
from services.db import create_services_table
import logging as log
from db.connection import db_con


def setup_db():
    log.info("setting up db")
    create_devices_table()
    create_schedules_table()
    create_watchers_table()
    create_watchers_mapping_table()
    create_services_table()
    log.info("db set up successfully")
    db_con.commit()
