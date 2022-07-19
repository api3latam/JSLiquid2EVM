# Server and Management Examples

### Basic Workflow
This includes the minimum components that are required for a basic servicing.
This have yet to include the Event listener that will be explained later. Or you can use it to programatically interact with a Liquid node.

```
import logging
from liquid.server import Service
from liquid.management import Wallet

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    server = Service(new_node=False)
    wallet = Wallet(server.get_proxy(), with_address=False)
```