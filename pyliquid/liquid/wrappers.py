import subprocess
import json
from typing import Callable, Optional, Union
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
    def wrap(obj, _caller: Callable, *args):
        """
        Internal function that handles RPC errors.

        Parameters
        ----------
        obj: cls
            Class object from which the method is being call.
        _caller: Callable
            The actual instance method to use for execution.
        args:
            Parameter for `_caller` function.

        Returns
        -------
        Any
            Output from RPC call.
        """
        try:
            return _func(obj, _caller, args)
        except JSONRPCException as json_exception:
            logging.error(f"A JSON RPC Exception occured: {json_exception}\n")
        except Exception as general_exception:
            logging.exception(f"An Exception occured: {general_exception}\n")
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
    def wrap(obj) -> Optional[Union[str, bytes]]:
        """
        Internal function that handles STDERR and STDOUT decoding.

        Returns
        -------
        Optional[Union[str, bytes]]
            Output from STDOUT.
        """
        try:
            cp = _func(obj)
            try:
                result = json.loads(cp.stdout)
            except json.JSONDecodeError:
                result = cp.stdout
            if not result:
                output = True
            else:
                output = result
            return output
        except subprocess.CalledProcessError as stderr:
            if stderr.output:
                logging.error(f"Command '{stderr.cmd}' return with error \
                    (code {stderr.returncode}): {stderr.output}\n")
                raise RuntimeError
            else:
                logging.warning(f"Skipping exception code \
                    ({stderr.returncode}) with no output error...\n")
    return wrap
