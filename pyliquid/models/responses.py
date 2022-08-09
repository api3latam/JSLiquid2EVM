"""
Defines models for server responses.
"""

from typing import Optional

from pydantic import BaseModel

class SuccessGet(BaseModel):
    """
    Model for successfull `get` requests.
    """
    status: int
    payload: Optional[str] = None