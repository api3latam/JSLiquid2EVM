from pathlib import Path
import logging

from typing import Callable

from bitcoinrpc.authproxy import JSONRPCException

REPO_NAME = 'PyLiquid2EVM'


def get_root() -> str:
    """
    Get the absolute path to the directory

    Returns
    -------
    str
        Root path of repository.
    """
    _path = str(Path(__file__)).split('/')
    for i in range(1, len(_path)):
        if _path[-i] == REPO_NAME:
            index = i
            break
    try:
        output = '/'.join(_path[:-index + 1])
    except NameError:
        logging.error('The given Repository was not found')
    return output


def rpc_exec(_func: Callable) -> Callable:
    """
    Wrapper for RPC functions calling, simplifying error management.  
    """
    def wrap(*args, **kwargs):
        try:
            return _func(args, kwargs)
        except JSONRPCException as json_exception:
            logging.error(f"A JSON RPC Exception occured: {json_exception}")
        except Exception as general_exception:
            logging.exception(f"An Exception occured: {general_exception}")
    return wrap
