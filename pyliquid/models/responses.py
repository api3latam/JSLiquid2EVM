"""
Defines models for server responses.
"""

from typing import Optional

from pydantic import BaseModel

class SuccessGet(BaseModel):
    """
    Model for successful `get` requests.
    """
    status: int
    payload: Optional[str] = None

class SuccessPost(BaseModel):
    """
    Model for successful `post` requests
    """
    status: int
    params: dict = {"description": "Fulfilled request!"}
