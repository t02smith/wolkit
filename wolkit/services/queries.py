from sqlalchemy.orm import Session
from services.err import *
from services.model import Service as ServiceModel, services, enable_all_services, enable_service, disable_service, \
    disable_all_services


def get_all_services(db: Session):
    return db.query(ServiceModel).all()


def set_service(service_name: str, new_value: bool, db: Session):
    service: ServiceModel = db.query(ServiceModel).filter(ServiceModel.name == service_name).first()
    if not service:
        raise ServiceNotFoundError(service_name)

    if new_value == service.active:
        raise ServiceAlreadyEnabledError(service_name) if service.active else ServiceAlreadyDisabledError(service_name)

    if new_value:
        enable_service(service_name)
    else:
        disable_service(service_name)

    service.active = new_value
    db.commit()
    db.refresh(service)


def set_all_services(new_value: bool, db: Session):
    services_ls = db.query(ServiceModel).all()
    for s in services_ls:
        s.active = new_value

    if new_value:
        enable_all_services(db)
    else:
        disable_all_services()

    db.commit()


def restart_service(service_name: str, db: Session):
    service: ServiceModel = db.query(ServiceModel).filter(ServiceModel.name == service_name).first()
    if not service:
        raise ServiceNotFoundError(service_name)

    if service.active:
        disable_service(service_name)

    if not service.active:
        service.active = True
        db.commit()
        db.refresh(service)

    enable_service(service_name, db)


def restart_all_services(db: Session):
    for service_name, data in services.items():
        restart_service(service_name, db)
