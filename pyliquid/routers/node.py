"""
Set of endpoints for managing the Liquid node.
"""

from fastapi import APIRouter, HTTPException, status

from .share import RESPONSES
from pyliquid.liquid.server import Service
from pyliquid.models import requests, responses

router = APIRouter(
    prefix="/node",
    tags=["node"],
    responses=RESPONSES
)

@router.post("/start")
async def get_node_status():
    """
    Get the status of `elementsd` daemon.
    """
    return Service._is_running()


def start_node():
    """
    Start a running instance of Liquid network.
    """
    _ = Service()
    return 'Service sucessfully created'