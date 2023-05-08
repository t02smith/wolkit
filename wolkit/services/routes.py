from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from auth.token import get_current_user
from auth.model import User
from db.connection import get_db
from services import queries as ser_db
from typing import List
import services.model as services

services_router = APIRouter(prefix="/services")


@services_router.get(
    "/",
    status_code=200,
    tags=["Services"],
    description="Returns the list of services, a brief description and whether they're active"
)
async def get_service_info(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ser_db.get_all_services(db)


@services_router.post(
    "/{service_name}/enable",
    status_code=201,
    tags=["Services"]
)
async def enable_service(service_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        ser_db.set_service(service_name, True, db)
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
async def enable_all_services(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.set_all_services(True, db)
    services.enable_all_services()
    return {
        "message": f"All services enabled"
    }


@services_router.post(
    "/{service_name}/disable",
    status_code=201,
    tags=["Services"]
)
async def disable_service(service_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        ser_db.set_service(service_name, False, db)
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
async def disable_all_services(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.set_all_services(False, db)
    services.disable_all_services()
    return {
        "message": f"All services disabled"
    }
