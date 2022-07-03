import logging
from liquid.server import Service
from liquid.management import Wallet

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    server = Service(new_node=False)
    wallet = Wallet(server.get_proxy(), with_address=False)
    out = wallet.list_wallets()
    print(out)
