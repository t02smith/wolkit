from typing import List

from fastapi import APIRouter, Depends

from auth.model import User
from auth.token import get_current_user
from services.environment.schema import EnvironmentListener

env_router = APIRouter(prefix="/environment")


@env_router.post(
    "/watch",
    status_code=201,
    description="Here you can add a new environment listener that will consider various external factors to wake a "
                "device. The following fields are available\n1. Temperature 'temperature'\n"
                "2. Light 'light'\n3. Noise 'noise'\n4. Proximity 'proximity'\nIt is recommended that you use the "
                "example python files from Pimorini to find values for these that suit your neeeds",
    summary="Add a new environment listener",
    tags=["Environment"]
)
async def new_environmental_factor(factor: EnvironmentListener, user: User = Depends(get_current_user)):
    return factor


@env_router.get(
    "/watch",
    status_code=200,
    description="Get a list of all the environment listeners you have recorded",
    summary="Get environment listeners",
    response_model=List[EnvironmentListener],
    tags=["Environment"]
)
async def get_env_listeners(user: User = Depends(get_current_user)):
    return []


@env_router.put(
    "/watch",
    status_code=200,
    description="Edit an existing environment listener",
    response_model=EnvironmentListener,
    tags=["Environment"]
)
async def update_env_listener(listener_id: int, ln: EnvironmentListener, user: User = Depends(get_current_user)):
    return ln
