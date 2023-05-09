from fastapi import APIRouter
from router.app import app
from auth.routes import auth_router
from devices.routes import devices_router
from services.routes import services_router
from services.wireless.routes import watchers_router

router = APIRouter(prefix="/api/v1")
router.include_router(devices_router)
router.include_router(watchers_router)
router.include_router(services_router)
router.include_router(auth_router)

app.include_router(router)



