from db.connection import Base, engine


def setup_db():
    print("Setting up DB")
    Base.metadata.create_all(bind=engine)

