from typing import Any

from pydantic import BaseModel


class GenericResponse(BaseModel):
    message: str