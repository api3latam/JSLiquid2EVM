
from uuid import uuid4
import json
from typing import Optional

from bitcoinrpc.authproxy import AuthServiceProxy  # type: ignore
from mnemonic import Mnemonic  # type: ignore
from liquid.wrappers import cli_exec, rpc_exec


class Wallet():
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
                 with_address: bool = True) -> None:
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
            output = self.proxy.getnewaddress()
            return output
        else:
            return creation

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

    @cli_exec
    def transfer_assets(self) -> json:
        """
        """
        pass


class Pool:
    """
    Object representing a unique pool of a token class

    Attributes
    ----------
    """

    def __init__(self, input_wallet: Wallet):
        self._vault_wallet = input_wallet

    @property
    def vaul_wallet(self):
        return self._vault_wallet

    def issue_token(self):
        """
        """
        pass

    def burn_token(self):
        """
        """
        pass
