from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from auth.token import get_current_user
from auth.model import User
from db.connection import get_db
from services import queries as ser_db
from typing import List
import services.model as services
from services.schema import Service as ServiceSchema
from router.responses import GenericResponse

services_router = APIRouter(prefix="/services")


@services_router.get(
    "/",
    status_code=200,
    tags=["Services"],
    response_model=List[ServiceSchema],
    description="Returns the list of services, a brief description and whether they're active"
)
async def get_service_info(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ser_db.get_all_services(db)


@services_router.post(
    "/all/enable",
    status_code=201,
    tags=["Services"],
    response_model=GenericResponse
)
async def enable_all_services(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.set_all_services(True, db)
    return GenericResponse(message=f"All services enabled")


@services_router.post(
    "/{service_name}/enable",
    status_code=201,
    tags=["Services"],
    response_model=GenericResponse
)
async def enable_service(service_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.set_service(service_name, True, db)
    return GenericResponse(message=f"Service {service_name} enabled")


@services_router.post(
    "/all/disable",
    status_code=201,
    tags=["Services"],
    response_model=GenericResponse
)
async def disable_all_services(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.set_all_services(False, db)
    return GenericResponse(message=f"All services disabled")


@services_router.post(
    "/{service_name}/disable",
    status_code=201,
    tags=["Services"],
    response_model=GenericResponse
)
async def disable_service(service_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.set_service(service_name, False, db)
    return GenericResponse(message=f"Service {service_name} disabled")


@services_router.post(
    "/all/restart",
    status_code=200,
    tags=["Services"],
    response_model=GenericResponse,
    name="Restart all services",
    description="Restart all running services. If a service has not been started then it will be enabled."
)
async def restart_all_service(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.restart_all_services(db)
    return GenericResponse(message="Restarted all services")


@services_router.post(
    "/{service_name}/restart",
    status_code=200,
    tags=["Services"],
    response_model=GenericResponse,
    name="Restart a service",
    description="Restart a running service. If the service has not been started then it will be enabled."
)
async def restart_service(service_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ser_db.restart_service(service_name, db)
    return GenericResponse(message=f"Restarted service {service_name}")
