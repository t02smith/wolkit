from fastapi import APIRouter
from routes.devices import devices_router

router = APIRouter(prefix="/api/v1")
router.include_router(devices_router)
