"""
Temporary solution to keep in memory interfaces to interact with the
background objects.
"""

import logging
from bitcoinrpc.authproxy import AuthServiceProxy # type: ignore

from pyliquid.liquid.server import Service
from pyliquid.liquid.management import Wallet

ACTIVE_SERVICE = {}  # {Service: AuthServiceProxy}
SESSION_WALLETS = []


def get_active_service() -> dict:
    """
    Retrieve latest state from service list.

    Returns
    -------
    dict
        Dict of Service instances and Proxy Services running with the API.
    """
    global ACTIVE_SERVICE
    return ACTIVE_SERVICE


def update_active_service(input_service: dict) -> None:
    """
    Updates ACTIVE_SERVICE dict from any scope in the code.

    Parameters
    ----------
    input_service: dict[Service, AuthServiceProxy]
        Dictionary to update current globals with.
    """
    global ACTIVE_SERVICE
    try:
        if len(input_service.keys()) != 1:
            raise KeyError
        elif not(isinstance(list(input_service.keys())[-1], Service)
           and isinstance(list(input_service.values())[-1], AuthServiceProxy)):
            raise TypeError
        ACTIVE_SERVICE.update(input_service)
    except (KeyError, TypeError):
        logging.error('The provided dictionary is not valid.')


def get_session_wallets() -> list:
    """
    Retrive the active list of initialized wallets for this session.

    Returns
    ------
    list[Wallets]
        List of Wallets for current API running session.
    """
    global SESSION_WALLETS
    return SESSION_WALLETS


def update_sessions_wallets(new_wallet) -> None:
    """
    Update SESSION_WALLETS list from any scope in the code.

    Parameters
    ----------
    new_wallet: Union[Wallet, list[Wallet]]
        The new instances to be added to current list on active sessions.
    """
    global SESSION_WALLETS
    try:
        if isinstance(list) and \
                any([isinstance(w, Wallet) for w in new_wallet]):
            SESSION_WALLETS.extend(new_wallet)
        elif isinstance(Wallet):
            SESSION_WALLETS.extend([new_wallet])
        else:
            raise TypeError
    except TypeError:
        logging.error('The provided object is not of valid type Wallet.')