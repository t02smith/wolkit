from sqlalchemy.orm import Session
import logging as log
from db.connection import db_con, Base, engine

Base.metadata.create_all(bind=engine)

def setup_db(db: Session):
    log.info("setting up db")

    log.info("db set up successfully")
    # db_con.commit()
