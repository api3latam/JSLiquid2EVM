"""
Set of endpoints for healtchecks.
"""

from fastapi import APIRouter, HTTPException, status

from .share import RESPONSES
from pyliquid.liquid.server import Service
from pyliquid.models.responses import SuccessGet

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses=RESPONSES
)


@router.get("/", tags=["node"])
async def node_health_status():
    """
    Check if there's any Liquid node running.

    Returns
    -------
    AuthServiceProxy
        Latest Proxy Service instance.
    """
    if Service._is_running():
        return SuccessGet(status=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=400, detail="Node is not running")
