from pydantic import BaseModel
from enum import Enum


class EnvironmentalFactor(Enum):
    LIGHT = "light"
    PROXIMITY = "proximity"
    NOISE = "noise"
    TEMPERATURE = "temperature"


class EnvironmentListenerBase(BaseModel):
    above_or_below_threshold: bool
    environmental_factor: EnvironmentalFactor
    threshold: float
    device_id: int


class EnvironmentListener(EnvironmentListenerBase):
    pass


class EnvironmentListenerCreate(EnvironmentListenerBase):
    pass
