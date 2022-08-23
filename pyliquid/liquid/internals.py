from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from .server import DEFAULT_LOCATION, Service
from .management import Wallet
from ..state import get_active_service, update_active_service, \
    get_session_wallets

router = APIRouter(prefix="/internal", tags=['management'],
                   responses={403: {"description": "Operation forbidden"},
                              404: {"description": "Not found"}})


class ServiceParams(BaseModel):
    new_node: Optional[bool] = True
    working_dir: Optional[str] = DEFAULT_LOCATION


def _check_for_proxy():
    """
    Check if there's any Service instance running to get its proxy.

    Returns
    -------
    AuthServiceProxy
        Latest Proxy Service instance.
    """
    _temp = get_active_service()
    if _temp:
        return list(_temp.values())[-1]
    else:
        _service = Service()
        _proxy = _service.get_proxy()
        update_active_service({_service: _proxy})
        _check_for_proxy()


@router.get('/wallet', tags=['wallet'])
async def get_wallet():
    """
    List active wallets on the node.
    """
    session_wallets = get_session_wallets()
    if session_wallets:
        _wallet = session_wallets[-1]
    else:
        _proxy = _check_for_proxy()
        _wallet = Wallet(_proxy)
    _wallet.list_wallets()


@router.get('/wallet/{requested_label}', tags=['wallet'])
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


@router.post('/wallet/create', tags=['wallet'])
async def post_create_wallet():
    """
    Creates a new Wallet instance
    """
    _proxy = _check_for_proxy()
    out = Wallet(_proxy, mode='c', with_address=False)
    return out


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
    _ = Service(**body)
    return {"description": "Service sucessfully created"}
