import sys
from pathlib import Path
import functools
from typing import Optional, Union

from dotenv import dotenv_values  # type: ignore


Config = dict[str, Optional[str]]


def get_root_path(root_dir_name: Union[str, Path]) -> str:
    """
    Get working directory for project root independently of user.

    Parameters
    ----------
    root_dir_name: Union[str, Path]
        The path to be used as root for the operations of the library.
    Returns
    ------
    working_dir: str
        Full path to working directory.
    """
    _error_message = "The specified path hasn\'t been added to path\
                yet. Please `set_working_path` prior."
    filtered_paths = list(filter(lambda x: str(root_dir_name) in x,
                                 sys.path))
    if len(filtered_paths) == 1:
        return filtered_paths[0]
    elif len(filtered_paths) > 1:
        return functools.reduce(lambda x, y:
                                x if len(x.split('/')) < len(y.split('/'))
                                else y, filtered_paths)
    else:
        raise KeyError(_error_message)


def set_working_path(target_paths: Union[str, list] = None) -> None:
    """
    Add to path the target routes passed down which are also included inside
    the repository folder.

    Parameters
    ----------
    target_paths: Union[str, list], default=None
        Folder(s) and/or file(s) to be included in path.
        When default, still appends root directory to path.
    """
    _error_message = 'The provided path(s) is not from a valid type.'
    if isinstance(target_paths, list):
        for t_path in target_paths:
            if isinstance(t_path, str) or isinstance(t_path, Path):
                sys.path.insert(0, str(t_path))
            else:
                raise TypeError(_error_message)
    elif isinstance(target_paths, str) or isinstance(target_paths, Path):
        sys.path.insert(0, target_paths)
    else:
        raise TypeError(_error_message)


def get_configs(file_path: str,
                keys: Optional[list[str]] = None) -> Config:
    """
    Load dictionary of environment variables.

    Parameters
    ----------
    env_path: str
        Location of .env file.
    keys: list, default = None
        Specific keys to return from .env file.

    Returns
    -------
    dict
        Configuration dictionary with all or indicated definitions from
        `.env` file.
    """
    envs = dotenv_values(file_path)
    if not keys:
        return envs
    else:
        return {k: v for k, v in envs.items() if k in keys}
