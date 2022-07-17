
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

    #TODO: Test this approach
    @rpc_exec
    def load_wallet(self, label: str) -> dict:
        """
        Load a wallet with a given label.

        Parameters
        ----------
        label: str
            Label of the wallet to be loaded.

        Returns
        -------
        dict
            Dictionary with a lists of wallets 
        """
        return self.proxy.loadwallet(label)
        

    #TODO: Test this approach
    @rpc_exec
    def get_balance(self) -> dict:
        """
        Get the balance of the current wallet.

        Returns
        -------
        dict
            Dictionary with a lists of wallets 
        """
        return self.proxy.getbalance()

    @rpc_exec
    def get_address(self) -> str:
        """
        Get the current address of the wallet.

        Returns
        -------
        str
            Current address of the wallet.
        """
        return self.proxy.getaddress()
    @rpc_exec
    def get_private_key(self) -> str:
        """
        Get the current private key of the wallet.

        Returns
        -------
        str
            Current private key of the wallet.
        """
        return self.proxy.dumpprivkey()
    @rpc_exec
    def get_public_key(self) -> str:
        """
        Get the current public key of the wallet.

        Returns
        -------
        str
            Current public key of the wallet.
        """
        return self.proxy.getpubkey()
    @rpc_exec
    def get_wallet_info(self) -> dict:
        """
        Get the current wallet information.

        Returns
        -------
        dict
            Current wallet information.
        """
        return self.proxy.getwalletinfo()
    @rpc_exec
    def send_to_address(self, address: str, amount: float) -> str:
        """
        Send a transaction to a given address.

        Parameters
        ---------
        address: str
            Address to send the transaction to.
        amount: float
            Amount to send.

        Returns
        -------
        str
            Transaction ID.
        """
        return self.proxy.sendtoaddress(address, amount)
    @rpc_exec
    def send_to_many(self, addresses: dict) -> str:
        """
        Send a transaction to multiple addresses.

        Parameters
        ---------
        addresses: dict
            Dictionary with addresses and amounts to send.

        Returns
        -------
        str
            Transaction ID.
        """
        return self.proxy.sendmany("", addresses)
    @rpc_exec
    def send_from_address(self, address: str, amount: float) -> str:
        """
        Send a transaction from a given address.

        Parameters
        ---------
        address: str
            Address to send the transaction from.
        amount: float
            Amount to send.

        Returns
        -------
        str
            Transaction ID.
        """
        return self.proxy.sendfrom(address, address, amount)

    @rpc_exec
    def issue_asset(self, name: str, quantity: int,
                     description: str, divisible: bool) -> str:
          """
          Issue an asset to the network.
    
          Parameters
          ---------
          name: str
                Name of the asset.
          quantity: int
                Quantity of the asset.
          description: str
                Description of the asset.
          divisible: bool
                If the asset is divisible.
    
          Returns
          -------
          str
                Transaction ID.
          """
          return self.proxy.issue(name, quantity, description, divisible)
#Create a object represnting a unique pool of a token class
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

    def issue_token(self, name: str, quantity: int,
                        description: str, divisible: bool) -> str:
            """
            Issue a token to the pool.
    
            Parameters
            ----------
            name: str
                Name of the token.
            quantity: int
                Quantity of the token.
            description: str
                Description of the token.
            divisible: bool
                If the token is divisible.
    
            Returns
            -------
            str
                Transaction ID.
            """
            return self._vault_wallet.issue_asset(name, quantity, description, divisible)
    def burn_token(self, name: str, quantity: int) -> str:
        """
        Burn a token from the pool.

        Parameters
        ----------
        name: str
            Name of the token.
        quantity: int
            Quantity of the token.

        Returns
        -------
        str
            Transaction ID.
        """
        return self._vault_wallet.burn_asset(name, quantity)

    