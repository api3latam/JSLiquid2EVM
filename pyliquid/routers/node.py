"""
Set of endpoints for managing the Liquid node.
"""

from fastapi import APIRouter, HTTPException, status

from pyliquid.routers.share import RESPONSES
from pyliquid.liquid.server import Service
from pyliquid.models import requests, responses

router = APIRouter(
    prefix="/node",
    tags=["node"],
    responses=RESPONSES
)

@router.post("/restart")
def restart_node():
    """
    Restart the running instance of Liquid node.
    """
    _ = Service()
    return responses.SuccessPost(status.HTTP_201_CREATED)