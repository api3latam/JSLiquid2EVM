# ^[A-z]*.elements.conf$
Set of example configuration files for interacting with the liquid node trough elements-cli.
Copy and paste them in your local config file based on your needs.
- Regtest: For local node, without bitcoin peg-in [no need to have a bitcoin node]. Useful for basic unit testing.
- Testnet: For liquid testnet. Note that is a standalone blockchain and not a pegged sidechain. Useful for basic integration testing.

# nginx.conf
This is a configuration file for serving the FastAPI app on a web server.
Contains basic setup for reverse proxy settings.
For usage, just make sure to change the `server_name` which is the exposed IP where
users will access the endpoints.

# supervisor.conf
This configuration file is for the process manager app.
Contain definitions about API initialization and directories for std outputs.
To make use of the file just replace with valid paths based on your server and os needs.
