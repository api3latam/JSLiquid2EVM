"""
Set of endpoints for operations with Liquid.
"""

import json
import logging
from typing import Optional, Union
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from pyliquid.routers.share import RESPONSES
from pyliquid.liquid.server import Service
from pyliquid.liquid.operations import Wallet
from pyliquid.models import responses
from pyliquid.utils.data import parse_decimal_to_float

router = APIRouter(
    prefix="/operations",
    responses=RESPONSES
)

class SendTx(BaseModel):
    target_address: str
    total_amount: Union[str, float]


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

@router.get("/wallet", tags=["wallet"])
async def get_wallet():
    """
    List active wallets on the node.

    TODO: This should only be callable by admin.
    """
    try:
        _instance = get_wallet_instance('r')
        output = _instance.list_wallets()
        print(f"The output is: {output}\n")
        return responses.SuccessGet(status=status.HTTP_200_OK, 
                                    payload=json.dumps(output))
    except Exception as exp:
        logging.error(exp)
        raise HTTPException(500)

@router.get("/wallet/", tags=["wallet"])
async def get_labeled_wallet(wallet_label: str):
    """
    Returns an specific wallet metadata.
    """
    try:
        _instance = get_wallet_instance('l', wallet_label)
        return responses.SuccessGet(status=status.HTTP_200_OK,
                        payload=json.dumps(parse_decimal_to_float(
                                                _instance.get_wallet_info())))
    except Exception as exp:
        logging.error(exp)
        raise HTTPException(500)

@router.post("/wallet/create", tags=["wallet"])
async def post_create_wallet():
    """
    Creates a new Wallet instance

    TODO: Only callable by admin.
    """
    try:
        _instance = get_wallet_instance('c')
        return responses.SuccessPost(status=status.HTTP_200_OK,
                                payload=json.dumps(
                                    parse_decimal_to_float(
                                        _instance.get_wallet_info())))
    except Exception as exp:
        logging.error(exp)
        raise HTTPException(500)

@router.post("/tx/send", tags=["tx"])
async def post_send_transaction(incoming_body: SendTx):
    """
    Send tokens from the node Wallet to given address.
    """
    try:
        _instance = get_wallet_instance('r')
        return responses.SuccessPost(status=status.HTTP_200_OK,
                                payload=json.dumps(
                                    _instance.send_to_address(
                                        incoming_body.target_address, 
                                        incoming_body.total_amount)))
    except Exception as exp:
        logging.error(exp)
        raise HTTPException
