from liquid.internals import Wallet, Liquid

if __name__ == "__main__":
    prox = Liquid.get_proxy()
    w = Wallet(prox, with_address=False)
    print(w.list_wallets())