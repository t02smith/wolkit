from fastapi import FastAPI
from db.setup import setup_db
from services.model import start_services


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
async def startup():
    setup_db()
    start_services()


