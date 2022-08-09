"""
Set of endpoints for operations with Liquid.
"""

import json
from fastapi import APIRouter, HTTPException, status

from .share import RESPONSES
from pyliquid.liquid.server import Service
from pyliquid.liquid.operations import Wallet
from pyliquid.models import requests, responses

router = APIRouter(
    prefix="/operations",
    responses={RESPONSES}
)

@router.get("/wallet", tags=["wallet"])
async def get_wallet():
    """
    List active wallets on the node.
    """
    try:
        _proxy = Service.get_proxy()
        _wallet = Wallet(_proxy, True)
        output = _wallet.list_wallets()
        return responses.SuccessGet(status.HTTP_200_OK, 
            json.dumps(output))
    except Exception:
        raise HTTPException(500)


async def get_labeled_wallet(requested_label: str):
    """
    Returns an specific wallet metadata.
    """
    session_wallets = get_session_wallets()
    if not session_wallets:
        raise RuntimeError('No wallet instance have been loaded. Please load\
            a wallet beforehand.')
    else:
        target_wallet = [w for w in session_wallets
                         if w.wallet['label'] == requested_label]
        if target_wallet:
            _wallet = target_wallet[-1]
            return _wallet.wallet
        else:
            raise TypeError('The requested address has not been loaded.')


async def post_create_wallet():
    """
    Creates a new Wallet instance
    """
    out = Wallet()
    return out