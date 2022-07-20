import logging
from fastapi import FastAPI

from pyliquid.liquid import internals

app = FastAPI()

app.include_router(internals.router)


@app.on_event('startup')
async def startup_event():
    """
    Startup script to be executed when API is initialized.
    """
    logging.basicConfig(level=logging.INFO)


@app.get('/')
async def root() -> dict[str]:
    """
    Root route of API functions. Just returns a message.

    Returns
    -------
    dict[str]
    """
    return {"message": "This is a Liquid API from API Latam."}
