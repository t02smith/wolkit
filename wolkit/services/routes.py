from fastapi import APIRouter, HTTPException, Depends

from auth.token import get_current_user
from auth.model import User
from services import db as ser_db
from typing import List
import services.services as services

services_router = APIRouter(prefix="/services")


@services_router.get(
    "/",
    status_code=200,
    tags=["Services"],
    response_model=List[services.Service],
    description="Returns the list of services, a brief description and whether they're active"
)
async def get_service_info(user: User = Depends(get_current_user)):
    return ser_db.get_services()


@services_router.post(
    "/{service_name}/enable",
    status_code=201,
    tags=["Services"]
)
async def enable_service(service_name: str, user: User = Depends(get_current_user)):
    try:
        ser_db.set_service(service_name, True)
        services.enable_service(service_name)
        return {
            "message": f"Service {service_name} enabled"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@services_router.post(
    "/all/enable",
    status_code=201,
    tags=["Services"]
)
async def enable_all_services(user: User = Depends(get_current_user)):
    ser_db.set_all_services(True)
    services.enable_all_services()
    return {
        "message": f"All services enabled"
    }


@services_router.post(
    "/{service_name}/disable",
    status_code=201,
    tags=["Services"]
)
async def disable_service(service_name: str, user: User = Depends(get_current_user)):
    try:
        ser_db.set_service(service_name, False)
        services.disable_service(service_name)
        return {
            "message": f"Service {service_name} enabled"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@services_router.post(
    "/all/disable",
    status_code=201,
    tags=["Services"]
)
async def disable_all_services(user: User = Depends(get_current_user)):
    ser_db.set_all_services(False)
    services.disable_all_services()
    return {
        "message": f"All services disabled"
    }
