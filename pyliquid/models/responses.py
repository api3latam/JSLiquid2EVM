"""
Defines models for server responses.
"""

# General imports
from typing import Optional, Union
import json
from pydantic import BaseModel

class SuccessGet(BaseModel):
    """
    Model for successful `get` requests.
    """
    status: int
    payload: Optional[str] = json.dumps({"description": "Successful request!"})

class SuccessPost(BaseModel):
    """
    Model for successful `post` requests
    """
    status: int
    payload: Optional[str] = json.dumps({"description": "Request fulfilled!"})
