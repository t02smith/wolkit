from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.connection import *
from db.setup import setup_db

with open("static/description.md", "r") as f:
    description = f.read()

app = FastAPI(
    title="Wake-on-LAN Kit",
    description=description,
    version="0.1",
    contact={
        "name": "Tom Smith",
        "email": "tcs1g20@soton.ac.uk"
    },
    openapi_tags=[
        {
            "name": "Scheduler",
            "description": "Schedule recurring times and days of the week for a device to wake up."
        },
        {
            "name": "Device Management",
            "description": "Manage your collection of wakeable devices. These are the ones that we will be waking up "
                           "for you."
        },
        {
            "name": "Watcher",
            "description": "Watch for nearby devices using WiFi and Bluetooth."
        },
        {
            "name": "Services",
            "description": "Enable or disable any background services, such as the Scheduler."
        },
        {
            "name": "Users",
            "description": "Relates to the users in the application. There will only be a singular admin user who has "
                           "permission to do everything. It is recommended that they change their password immediately."
        }
    ],
    debug=True
)


@app.on_event("startup")
async def start_services(db: Session = Depends(get_db)):
    setup_db(db)
    # services = get_services()
    # for s in services:
    #     if s.active:
    #         enable_service(s.name)
