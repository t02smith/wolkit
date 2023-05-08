from fastapi import APIRouter

from wolkit.auth.routes import auth_router
from wolkit.devices.routes import devices_router
from wolkit.services.routes import services_router
from wolkit.services.wireless.routes import watchers_router

router = APIRouter(prefix="/api/v1")
router.include_router(devices_router)
router.include_router(watchers_router)
router.include_router(services_router)
router.include_router(auth_router)