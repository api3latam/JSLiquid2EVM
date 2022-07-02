"""
Sub module with everything related with serving and managing the underlying
infrastructure of a running Liquid node.
"""

import os
import subprocess
from datetime import datetime
import logging
from typing import Optional

from bitcoinrpc.authproxy import AuthServiceProxy  # type: ignore
from liquid.wrappers import cli_exec
from utils.misc import Config, get_configs

DEFAULT_LOCATION = f"{os.environ['HOME']}/.elements"


class Service():
    """
    Object representing set of functionalities to interact with the daemon.
    Including direct commands trough the command line for both the `elementsd`
    and `elements-cli`, and the RPC connection of the cli.
    """

    def __init__(self, new_node: Optional[bool] = True,
                 working_dir: Optional[str] = DEFAULT_LOCATION) -> None:
        """
        Constructor for Service class.

        Parameters
        ---------
        new_node: Optional[bool]
            If either create a new directory for the blockchain or use
            any already available for the mode set in config file.
        working_dir: Optional[str]
            If you want to use any other directory than the default one 
            at `$HOME/.elements`. This should be the same path that contains 
            the `elements.conf` file.
        """
        if new_node:
            self._check_location(working_dir)
            if self._is_running():
                logging.info("A daemon is already running...\n\
                    Stopping service...")
                _ = self._stop_daemon()
            if working_dir != DEFAULT_LOCATION:
                _ = self._start_daemon(working_dir)
            else:
                _ = self._start_daemon()
            logging.info("Elements Core up and running!")
        else:
            if self._is_running():
                logging.info("Daemon is running and no custom instructions\
                    were given. Seems good to go!")
            else:
                logging.info("Daemon is not running and `new_node` was set to\
                'False'. If you don't have a running service you'll be\
                    restricted on what you can do.")

    def _check_location(self, network_path: str) -> None:
        """
        Check the availability and information of the network trough its
        config file.

        Parameters
        ----------
        network_path: str
            The path that will be root for the operations.
            Including the `.conf` file and network directory.
        """
        try:
            with open(f"{network_path}/elements.conf", 'r') as confs:
                mode = [v for v in confs.readlines() if v.startswith('chain=')]
            logging.info(f"Initializating Chain in mode: \
                {mode[0].split('=')[-1]}\nLocated at directory: \
                    {network_path}/{mode[0]}")
        except FileNotFoundError:
            logging.error("Verify that there's a `.conf` file at the specified\
                            path")

    @classmethod
    @cli_exec
    def _is_running(cls) -> subprocess.CompletedProcess:
        """
        Check if the daemon is not already running.

        Returns
        -------
        subprocess.CompletedProcess
            Object with stdout that tells us if daemon is running or not.
        """
        cmd = "pgrep -u $USER 'elementsd'"
        return subprocess.run(cmd, capture_output=True, check=True, shell=True)

    @classmethod
    @cli_exec
    def _start_daemon(cls, input_path: Optional[str] = None) \
            -> subprocess.CompletedProcess:
        """
        Start a new elementsd daemon.

        Parameters
        ----------
        input_path: str
            Data directory for starting the service.

        Returns
        -------
        subprocess.CompletedProcess
            Object with stdout that tells us if the daemon started.
        """
        if input_path:
            cmd = f"elementsd -datadir={input_path}"
        else:
            cmd = "elementsd"  # Defaults to `DEFAULT_LOCATION` path.
        return subprocess.run(cmd, capture_output=True, check=True, shell=True)

    @classmethod
    @cli_exec
    def _stop_daemon(cls) -> subprocess.CompletedProcess:
        """
        Stop a running instance of elementsd.

        Returns
        -------
        subprocess.CompletedProcess
            Object with stdout that tells us if the daemon stopped.
        """
        cmd = "elements-cli stop"
        return subprocess.run(cmd, capture_output=True, check=True, shell=True)

    @staticmethod
    def get_proxy(host: Optional[str] = 'localhost',
                  auth_dict: Optional[Config] = None) -> AuthServiceProxy:
        """
        Return RPC Connection instance with active node

        Parameters
        ----------
        host: str, default = 'localhost'
            The target host to use for the connection. Expects a full URL with
            its own credentials.
            Default 'localhost' targets `127.0.0.1`.
        auth_dict: Config, default = None
            Set of credentials to be used by proxy service. If `None`, uses
            default parameters from .env file.
            NOTICE: Only works when host is the default one.

        Returns
        -------
        AuthServiceProxy
            Authenticated Proxy Service object.
        """
        if (host != 'localhost') and (auth_dict):
            raise ValueError(
                'Either provide a custom host or parameters to be used by \
                `localhost`')
        else:
            if not auth_dict:
                auth_dict = get_configs(
                    keys=['rpc_port', 'rpc_user', 'rpc_password'])
            _cred = f"{auth_dict['rpc_user']}:{auth_dict['rpc_password']}"
            host = f"http://{_cred}@127.0.0.1:{auth_dict['rpc_port']}"
        asp = AuthServiceProxy(host)
        logging.info(f"[{datetime.now()}] Proxy service created at: {host}")
        return asp
