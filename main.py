from fastapi import FastAPI
from routes import router
import uvicorn
from db.setup import setup_db
from lib.schedule import schedule_watcher
import asyncio

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def start_schedule_watcher():
    asyncio.get_event_loop().create_task(schedule_watcher())

if __name__ == "__main__":
    setup_db()
    uvicorn.run("main:app", host="127.0.0.1", port=5055, reload=True)