from fastapi import FastAPI
from routes import router
import uvicorn
from db.setup import setup_db
from db.services import get_services
from lib.schedule import schedule_watcher
from net.sniffer import listen_for_packets
from net.wireless import watch_LAN
import asyncio

HOST_IP_ADDRESS: str = "192.168.43.75"
# target = 192.168.43.136

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def start_schedule_watcher():
    services = get_services()
    if services[0].active:
        asyncio.get_event_loop().create_task(schedule_watcher())

    if services[1].active:
        asyncio.get_event_loop().create_task(listen_for_packets(HOST_IP_ADDRESS))

    if services[2].active:
        asyncio.get_event_loop().create_task(watch_LAN())

if __name__ == "__main__":
    setup_db()
    uvicorn.run("main:app", host="127.0.0.1", port=5055, reload=True)