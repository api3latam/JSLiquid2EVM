import os
import subprocess
from datetime import datetime
import time
from uuid import uuid4
import json
import logging
from typing import NoReturn, Optional, Union

from bitcoinrpc.authproxy import AuthServiceProxy  # type: ignore
from mnemonic import Mnemonic  # type: ignore
from liquid.wrappers import rpc_exec, cli_exec
from utils.misc import Config, get_configs

DEFAULT_LOCATION = f"{os.environ['HOME']}/.elements"


class Serivce():
    """
    Object representing set of functionalities for interacting with the daemon.
    """

    def __init__(self, new_node: Optional[bool] = False, 
                working_dir: Optional[str] = DEFAULT_LOCATION) -> NoReturn:
        """
        Constructor for Service class

        Parameters
        ---------
        initialize: bool
            If a daemon hasn't been started yet, it spins it.
        
        """
        if not self._is_running():
            _daemon: Union[dict, str] = self._start_daemon()
            logging.info(_daemon)

    def _check_location(self, network_path: Optional[str]) -> bool:
        """
        Check the location for network workdir.
        """
        with open(f"{network_path}/elements.conf", 'r') as confs:
            mode = [v for v in confs.readlines() if v.startswith('chain=')]
        logging.info(f"Initializating Chain {mode[0]}")
        if os.path.isdir(f"{network_path}/{mode}"):
            _time = int(time.time())
            new_path = 
            os.mkdir(f"{network_path}/{mode}{_time}")

    @cli_exec
    def _is_running(self) -> subprocess.CompletedProcess:
        """
        Check if the daemon is not running already
        """
        cmd = "pgrep -u $USER \"elementsd\""
        return subprocess.run(cmd, capture_output=True, check=True, shell=True)

    @cli_exec
    def _start_daemon(self) -> subprocess.CompletedProcess:
        """
        Ensure that elementsd is currently running and that a fresh daemon
        is instanciated.

        Returns
        """
        cmd = ["elementsd"]
        return subprocess.run(cmd, capture_output=True, check=True, shell=True)

    def _generate_mnemonic(self, strength: Optional[int] = 256,
                           language: Optional[str] = "english") -> str:
        """
        Generate a mnemonic for wallet creation.

        Parameters
        ----------
        strength: int, default = 256
            The length for the resulting phrase to be generated. 
        language: str, default = "english"
            The language of the dictionary to be used.

        Returns
        -------
        str
            Resulting mnemonic phrase given its strenght.
        """
        mnemo = Mnemonic(language)
        return mnemo.generate(strength=strength)

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


class Wallet(Serivce):
    """
    Object representation for a unique wallet on the node.

    Attributes
    --------
    _proxy: AuthServiceProxy
        Authenticated Proxy Service to be used by the classmethods.
    _wallet: Dict
        Resulting metadata of created wallet at the network level.
    """

    _proxy: AuthServiceProxy
    _wallet: dict

    def __init__(self, proxy_service: AuthServiceProxy,
                 wallet_label: Optional[str] = None,
                 with_address: bool = True) -> NoReturn:
        """
        Constructor for Wallet class.

        Parameters
        ---------
        proxy: AuthServiceProxy
            Authenticated Proxy Service to be used by troughout the class.
        with_address: bool, default = True
            If your wallet should have at least one address.
        """
        self._proxy = proxy_service
        self._wallet = self._create_wallet(label=wallet_label,
                                           address=with_address)

    @property
    def proxy(self) -> AuthServiceProxy:
        """
        Current proxy service on use.
        """
        return self._proxy

    @property
    def wallet(self) -> dict:
        """
        Current wallet metadata at the network level.
        """
        return self._wallet

    def _create_wallet(self, label: str, address: bool) -> dict:
        """
        Create a wallet from a random name.

        Returns
        ------
        dict
            Resulting decoded JSON from method:
                `{name: str, warning: str}`
        """
        if not label:
            label = str(uuid4())
        creation = self.proxy.createwallet(label, False, False)
        if address:
            output = self.proxy.getaddress()
            return output
        else:
            return creation

    @rpc_exec
    def list_wallets(self) -> dict:
        """
        Get currently loaded wallets.

        Returns
        -------
        dict
            Dictionary with a lists of wallets 
        """
        return self.proxy.listwallets()

    @rpc_exec
    def _load_wallet(self) -> dict:
        """
        Load an existing wallet
        """
        pass

    @rpc_exec
    def get_balance(self, address: str) -> json:
        """
        Parameters
        ---------
        """
        pass


class Pool:
    """
    Object representing a unique pool of a token class

    Attributes
    ----------
    """
