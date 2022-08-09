"""
Utilities for data manipulation and validation
"""

import logging


def check_sorted_index_tuple(input_list: list[tuple]) -> bool:
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
