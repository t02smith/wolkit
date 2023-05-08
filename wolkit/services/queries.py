from sqlalchemy.orm import Session
from services.err import *
from services.model import Service as ServiceModel, services


def get_all_services(db: Session):
    return db.query(ServiceModel).all()


def set_service(service_name: str, new_value: bool, db: Session):
    service: ServiceModel = db.query(ServiceModel).filter(ServiceModel.name == service_name).first()
    if not service:
        raise ServiceNotFoundError(service_name)

    enabled = service.active == 1
    if new_value == enabled:
        raise ServiceAlreadyEnabledError(service_name) if enabled else ServiceAlreadyDisabledError(service_name)

    service.active = 1 if new_value else 0
    db.commit()
    db.refresh(service)


def set_all_services(new_value: bool, db: Session):
    services_ls = db.query(ServiceModel).all()
    for s in services_ls:
        s.active = 1 if new_value else 0

    db.commit()
