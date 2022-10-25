import os
from typing import Optional, Union

def get_configs(keys: Union[list[str], str]) -> Union[str, list[str]]:
    """
    Load dictionary of environment variables.

    Parameters
    ----------
    keys: Union[list[str], str]
        Specific keys to return from .env file.

    Returns
    -------
    Union[str, list[str]]
    """
    if (type(keys) == str):
        env_vals = os.environ[keys]
        return env_vals or ""
    elif (type(keys) == list):
        env_vals = [os.environ[k] for k in keys]
        return env_vals or [""]
    else:
        raise TypeError("The given type is not valid")
