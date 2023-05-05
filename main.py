from fastapi import FastAPI
from routes import router
import uvicorn
from db.setup import setup_db
from db.services import get_services
from lib.services import enable_service
import asyncio
import logging

HOST_IP_ADDRESS: str = "192.168.43.75"
# target = 192.168.43.136

app = FastAPI(
    title="Wake-on-LAN Kit",
    description="A toolkit for waking your LAN devices is various different ways. This includes: scanning your local "
                "network, looking for nearby bluetooth devices, scheduling devices, and more. This project is being "
                "submitted for the coursework for COMP3210 - Advanced Computer Networks at the University of "
                "Southampton.",
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
        }
    ],
    debug=True
)
app.include_router(router)


@app.on_event("startup")
async def start_services():
    services = get_services()
    for s in services:
        if s.active:
            enable_service(s.name)

if __name__ == "__main__":
    setup_db()
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run("main:app", host="127.0.0.1", port=5055, reload=True)