from curses.ascii import HT
import json
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Any, Optional

from .server import DEFAULT_LOCATION, Service
from .management import Wallet
from ..models import EncodedResponse

router = APIRouter(prefix="/internal", tags=['management'],
                   responses={403: {"description": "Operation forbidden"},
                              404: {"description": "Not found"}})


class ServiceParams(BaseModel):
    new_node: Optional[bool] = True
    working_dir: Optional[str] = DEFAULT_LOCATION


def get_wallet_instance(wallet_mode: str, 
                        target_label: Optional[str] = None) -> Wallet:
    """
    Return wallet instance depending on specified mode.
    """
    _proxy = Service.get_proxy()
    if target_label:
        return Wallet(_proxy, wallet_mode, target_label)
    else:
        return Wallet(_proxy, wallet_mode)

def encode_response_model(endpoint: str, status_code: int,
        input_payload: Any) -> str:
    """
    Encodes as a string a payload based on the `EncodedResponse` model.

    Parameters
    ----------
    payload: Any
        The main response object to be encoded.

    Returns
    -------
    str
        The encoded JSON string model object.
    """
    return json.dumps(
        EncodedResponse(
            endpoint_name=endpoint,
            status=status_code,
            payload={"result": input_payload}
        ).dict())

@router.get('/wallet', tags=['wallet'])
async def get_wallet(encoded: Optional[bool] = False):
    """
    List active wallets on the node.
    """
    try:
        _wallet = get_wallet_instance("r")
        output = _wallet.list_wallets()
        if encoded:
            return encode_response_model("/internal/wallet", status.HTTP_200_OK
                , output)
        else:
            return output
    except Exception as error:
        if encoded:
            raise HTTPException(status_code=500,
            detail={"encoded": True, "error": error})
        else:
            raise HTTPException(status_code=500,
            detail={"encoded": False, "error": error})


@router.post('/wallet/create', tags=['wallet'])
async def post_create_wallet():
    """
    Creates a new Wallet instance
    TODO: Only callable by admin.
    """
    try:
        _instance = get_wallet_instance('c')
        return _instance.wallet
    except Exception:
        raise HTTPException(500)


@router.get('/node/status', tags=['node'])
async def get_node_status():
    """
    Get the status of `elementsd` daemon.
    """
    if Service._is_running():
        return {"description": "Running and Healthy"}
    else:
        return {"description": "Node is not running"}


@router.post('/node/start', tags=['node'])
def start_node(body: ServiceParams):
    """
    Start a running instance of Liquid network.
    """
    _ = Service(new_node=body.new_node, working_dir=body.working_dir)
    return {"description": "Service sucessfully created"}
