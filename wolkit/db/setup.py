from sqlalchemy.orm import Session
from sqlalchemy import event
import logging as log
from db.connection import Base, engine


def setup_db(db: Session):
    log.info("setting up db")
    Base.metadata.create_all(bind=engine)
    log.info("db set up successfully")
