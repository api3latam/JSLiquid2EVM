"""
Set of functions for callbacks to interact with Liquid functionalities.
"""

from .server import Service
from .management import Wallet


async def check_for_proxy():
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


async def get_wallet():
    """
    List active wallets on the node.
    """
    session_wallets = get_session_wallets()
    if session_wallets:
        _wallet = session_wallets[-1]
    else:
        _proxy = _check_for_proxy()
        _wallet = Wallet(_proxy, with_address=False)
    _wallet.list_wallets()


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
