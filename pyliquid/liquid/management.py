"""
Core components that represent objects inside Liquid node like a Wallet.
"""
from uuid import uuid4
from typing import Optional, Callable

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
        Getter method for `proxy` attribute.
        """
        return self._proxy

    @property
    def wallet(self) -> dict:
        """
        Getter method for `wallet` attribute.
        """
        return self._wallet

    @classmethod
    @rpc_exec
    def _wrapper_executor(cls, _inst_func: Callable, *args):
        """
        Executor for wrapper functions to work withing instance methods.

        Parameters
        ---------
        _inst_func: Callable
            Instance function to be used.
        *args:
            Set of parameters to be passed down to the function.

        Returns
        -------
        dict
            Output of function execution.
        """
        if args:
            # Unpacks and unnest args before passing it down to function.
            return _inst_func(*args[0])
        else:
            return _inst_func()

    def _create_wallet(self, label: str, address: bool) -> dict:
        """
        Create a wallet from a random name.

        Parameters
        ----------
        label: str
            Name for the wallet
        address: bool
            Either to create or not an address for this wallet.

        Returns
        ------
        dict
            Resulting metadata from Wallet creation process.
        """
        if not label:
            label = str(uuid4())
        creation = self._wrapper_executor(self.proxy.createwallet, label,
                                          False, False)
        if address:
            output = self._wrapper_executor(self.proxy.getnewaddress)
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

    def list_wallets(self) -> list:
        """
        Get all saved wallets at network directory.

        Returns
        -------
        dict
            Dictionary with a lists of wallets.
        """
        return self._wrapper_executor(self.proxy.listwallets)

    @rpc_exec
    def _load_wallet(self):
        """
        """
        pass

    @rpc_exec
    def get_balance(self):
        """
        """
        pass

    @cli_exec
    def transfer_assets(self):
        """
        """
        pass


class Pool:
    """
    Object representing a unique pool of a token class.

    Attributes
    ----------
    _vault_wallet: Wallet
        Wallet owner of this Pool.
    """

    _vault_wallet: Wallet

    def __init__(self, input_wallet: Wallet):
        """
        Constructor for Pool class.

        Parameters
        ----------
        input_wallet: Wallet
            Wallet to own the Pool and safeguard the tokens.
        """
        self._vault_wallet = input_wallet

    @property
    def vaul_wallet(self):
        """
        Getter method for `vault_wallet` attribute.
        """
        return self._vault_wallet

    def issue_token(self):
        """
        """
        pass

    def burn_token(self):
        """
        """
        pass
