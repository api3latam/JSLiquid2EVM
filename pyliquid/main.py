import os
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def get_credentials():
    load_dotenv()
    return os.environ['rpc_user'], os.environ['rpc_password'], os.environ['rpc_port']

if __name__ == "__main__":
    rpc_user, rpc_password, rpc_port = get_credentials()
    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))

        result = rpc_connection.getwalletinfo()

        print(result["balance"]["bitcoin"])
    except JSONRPCException as json_exception:
        print("A JSON RPC Exception occured: " + str(json_exception))
    except Exception as general_exception:
        print("An Exception occured: " + str(general_exception))