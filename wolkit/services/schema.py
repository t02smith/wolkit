from pydantic import BaseModel


class Service(BaseModel):
    name: str
    description: str
    active: bool
