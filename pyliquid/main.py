from pathlib import Path
import logging
from fastapi import FastAPI

from pyliquid.routers import health, node, operations
from pyliquid.liquid import server
from pyliquid.utils import misc

PROJECT_PATH = "PyLiquid2EVM"

_base_path = str(Path(__file__)).split('/')
_filter_path = ['/'.join(_base_path[:i]) for i in range(1, len(_base_path))
                if PROJECT_PATH not in _base_path[:i]][-1]

BACKEND_PATH = f"{_filter_path}/{PROJECT_PATH}"

app = FastAPI()

app.include_router(health.router)
app.include_router(operations.router)
app.include_router(node.router)


@app.on_event('startup')
async def startup_event():
    """
    Startup script to be executed when API is initialized.
    """
    logging.basicConfig(level=logging.INFO)
    misc.set_working_path(BACKEND_PATH)
    server.Service()


@app.get('/')
async def root() -> dict[str]:
    """
    Root route of API functions. Just returns a message.

    Returns
    -------
    dict[str]
    """
    return {"message": "This is a Liquid Service build by API Latam."}
