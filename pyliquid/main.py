import logging
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from pyliquid.liquid import internals

app = FastAPI()

app.include_router(internals.router)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    """
    Handler for returned data from HTTP Exceptions.
    """
    if exc.detail['encoded']:
        return JSONResponse(
            status_code=exc.status_code,
            content=json.dumps({
                "message": exc.detail
            }
        ))
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={
            "message": exc.detail
        })

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
