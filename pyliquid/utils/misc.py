from pathlib import Path
import logging
from typing import Optional

from dotenv import dotenv_values  # type: ignore

REPO_NAME = 'PyLiquid2EVM'

Config = dict[str, Optional[str]]


def get_root() -> str:
    """
    Get the absolute path to the directory

    Returns
    -------
    str
        Root path of repository.
    """
    _path = str(Path(__file__)).split('/')
    for i in range(1, len(_path)):
        if _path[-i] == REPO_NAME:
            index = i
            break
    try:
        output = '/'.join(_path[:-index + 1])
    except NameError:
        logging.error('The given Repository was not found\n')
    return output


def get_configs(env_path: Optional[str] = None,
                keys: Optional[list[str]] = None) -> Config:
    """
    Load dictionary of environment variables

    Parameters
    ----------
    env_path: str, default = None
        Location of .env file. Defaults to repository root folder.
    keys: list, default = None
        Specific keys to return from .env file.

    Returns
    -------
    dict
        Configuration dictionary with all or indicated definitions from 
        `.env` file.
    """
    if not env_path:
        env_path = str(Path(get_root()).joinpath('.env'))
    envs = dotenv_values(env_path)
    if not keys:
        return envs
    else:
        return {k: v for k, v in envs.items() if k in keys}
