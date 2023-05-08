from typing import Any

from pydantic import BaseModel


class GenericResponse(BaseModel):
    message: str

    def __init__(self, message: str, **data: Any):
        super().__init__(**data)
        self.message = message
