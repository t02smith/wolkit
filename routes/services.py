from fastapi import APIRouter, HTTPException
import db.services as ser_db

services_router = APIRouter(prefix="/services")


@services_router.get("/", status_code=200, tags=["Services"])
async def get_service_info():
    return ser_db.get_services()


@services_router.post("/{service_name}/enable")
async def enable_service(service_name: str):
    pass


@services_router.post("/{service_name}/disable")
async def disable_service(service_name: str):
    pass
