from fastapi import APIRouter
from routes.devices import devices_router
from routes.watchers import watchers_router
from routes.services import services_router

router = APIRouter(prefix="/api/v1")
router.include_router(devices_router)
router.include_router(watchers_router)
router.include_router(services_router)