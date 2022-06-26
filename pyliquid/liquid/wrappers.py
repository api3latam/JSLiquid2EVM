import subprocess
import json
from typing import Callable
import logging

from bitcoinrpc.authproxy import JSONRPCException  # type: ignore


def rpc_exec(_func: Callable) -> Callable:
    """
    Wrapper for RPC functions calling, simplifying error management.

    Parameters
    ----------
    _func: Callable
        Function to be wrapped.

    Returns
    -------
    Callable
        Original function already wrapped.
    """
    def wrap():
        try:
            return _func()
        except JSONRPCException as json_exception:
            logging.error(f"A JSON RPC Exception occured: {json_exception}")
        except Exception as general_exception:
            logging.exception(f"An Exception occured: {general_exception}")
    return wrap


def cli_exec(_func: Callable) -> Callable:
    """"
    Wrapper for executing routines trough console.

    Parameters
    ----------
    _func: Callabe
        Function to be wrapped.

    Returns
    -------
    Callable
        Function executable already wrapped.
    """
    def wrap(cmd: str):
        """
        """
        try:
            cp = _func()
            try:
                result = json.loads(cp.stdout)
            except json.JSONDecodeError:
                result = cp.stdout
            return result
        except subprocess.CalledProcessError as stderr:
            logging.error(stderr)
    return wrap
