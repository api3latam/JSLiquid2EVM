from liquid.management import Wallet, Pool

async def request_check_balance(target_pool: Pool) -> dict:
    _wallet: Wallet = target_pool.vaul_wallet
    output: dict = _wallet.get_balance()
    return output