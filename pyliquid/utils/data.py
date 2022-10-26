"""
Utilities for data manipulation and validation
"""

import logging
from typing import Optional, List, Tuple
from decimal import Decimal


def check_sorted_index_tuple(input_list: List[Tuple]) -> Optional[bool]:
    """
    Verify if the input list is already sorted based on sub-indexes from
    tuple.

    Parameters
    ----------
    input_list: list[tuple]
        The giving tuple should have an index as its first value.

    Returns
    -------
    _is_sorted: bool
        Boolean value indicating if it was sorted or not.
    """
    try:
        index_list = [i[0] for i in input_list]
        return sorted(index_list) == index_list
    except TypeError:
        logging.error('It was not posisble to sort the list. \
            Review the given tuples.')

def parse_decimal_to_float(input_dict: dict) -> dict:
    """
    Cast any decimal type to floats or integer. 
    This enables `json` package to dumps responses from rpc response.

    Paramaters
    ----------
    input_dict: dict
        The raw data to be casted and formatted.

    Returns
    -------
    dict
        The resulting dictionary with compatible types.
    """
    to_return = {}
    for k, v in input_dict.items():
        if type(v) == Decimal:
            to_return[k] = float(v)
        elif type(v) == dict:
            to_return.update({k: parse_decimal_to_float(v)})
        else:
            to_return[k] = v
    return to_return
