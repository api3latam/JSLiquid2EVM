from typing import Union, Optional, NewType
import logging

from dotenv import dotenv_values
from bitcoinrpc.authproxy import AuthServiceProxy  # type: ignore

from utils import get_root

Config = NewType('Config', dict[str, Union[str, int, float]])


def get_configs(env_path: Optional[str] = None, keys: Optional[list[str]] = None) -> Config:
    """
    Load dictionary of environment variables

    Parameters
    ----------
    env_path: str, default = None
        Location of .env file. Defaults to repository root folder.
    keys: list, default = None
        Specific keys to return from .env file.

    Returns
    -------
    dict

    """
    if not env_path:
        env_path = (get_root()).joinpath('.env')
    envs = dotenv_values(env_path)
    if not keys:
        return envs
    else:
        return {k: v for k, v in envs.items() if k in keys}


def get_proxy(host: Optional[str] = 'localhost', auth_dict: Optional[Config] = None) -> AuthServiceProxy:
    """
    Return RPC Connection instance with active node

    Parameters
    ----------
    host: str, default = 'localhost'
        The target host to use for the connection. Expects a full URL with its own credentials.
        Default 'localhost' targets `127.0.0.1`.
    auth_dict: Config, default = None
        Set of credentials to be used by proxy service. If `None`, uses default parameters from .env file.
        Only works when host is the default one.

    Returns
    -------
    AuthServiceProxy
    """
    if (host != 'localhost') and (auth_dict):
        raise ValueError(
            'Either provide a custom host or parameters to be used by `localhost`')
    else:
        if not auth_dict:
            auth_dict = get_configs(
                keys=['rpc_port', 'rpc_user', 'rpc_password'])
        host = f"http://{auth_dict['rpc_user']}:{auth_dict['rpc_password']}@127.0.0.1:{auth_dict['rpc_port']}"
    asp = AuthServiceProxy(host)
    logging.info(f"Proxy service created at: {getattr(asp, '__service_url')}")
    return asp
