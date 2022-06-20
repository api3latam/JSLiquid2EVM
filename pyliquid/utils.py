from pathlib import Path
import logging
from typing import Union, Optional

REPO_NAME = 'PyLiquid2EVM'


def get_root(as_string: Optional[bool] = False) -> Union[str, Path]:
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
        return str(output) if as_string else Path(output)
    except NameError:
        logging.error('The given Repository was not found')
