"""
Defines models for server responses.
"""

from typing import Optional
from pydantic import BaseModel

class EncodedResponse(BaseModel):
    """
    Model for encoded responses for airnode.
    """
    endpoint_name: str
    status: int
    payload: Optional[dict] = {}
