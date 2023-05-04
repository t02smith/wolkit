from pydantic import BaseModel


class Service(BaseModel):
    """
    A service is a background task that will allow us to wake a device based
    upon a given condition.
    """
    name: str
    description: str
    active: bool
