from bitcoinrpc.authproxy import JSONRPCException  # type: ignore
from pyliquid.auth import get_proxy


if __name__ == "__main__":
    try:
        rpc_connection = get_proxy()

        result = rpc_connection.getwalletinfo()

        print(result["balance"]["bitcoin"])
    except JSONRPCException as json_exception:
        print("A JSON RPC Exception occured: " + str(json_exception))
    except Exception as general_exception:
        print("An Exception occured: " + str(general_exception))
