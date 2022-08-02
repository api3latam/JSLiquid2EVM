"""
Defines prototype for incoming data, and validators for fields prior to
execution.
"""

from datetime import datetime
from typing import Tuple
from pydantic import BaseModel, Field, validator

from ..utils.data import check_sorted_index_tuple


def check_matching_list_sequences(list_field: list[tuple], len_field: int) \
                                -> None:
    """
    Helper function for Instructions validators. Checks wether the length
    match across the given parameters.

    Parameters
    ----------
    list_field: list[tuple]
        Could be either `cmd` or `arg` from Instructions Model.
    len_filed: int
        Either the `seq` or the lenght from `cmd` to be matched with.
    """
    _is_sorted = check_sorted_index_tuple(list_field)
    if (len(list_field) != len_field) and (_is_sorted):
        raise ValueError("The number of commands does not the \
                expected sequence!")


class Instructions(BaseModel):
    """
    Data object for set of instructions to be executed by the backend.

    Attributes
    ----------
    seq: int
        The number of commands to expect.
    cmd: list[Tuple[int, str]]
        The names of the functions to be executed in its corresponding order.
    arg: list[Tuple[int, str | None]] | None, default=None
        The sequence of arguments to be used by the functions executions. If
        all the functions have no arguments then defauts to None, else even
        if only one of those have arguments, it should contain the order for
        which that parameters corresponds to and fill the rest with None.
    """

    seq: int
    cmd: list[Tuple[int, str]]
    arg: list[Tuple[int, str | None]] | None = None

    @validator('seq', pre=True, always=True)
    def seq_higher_than_zero(cls, v):
        """
        Validates that sequence is higher than 0. At least one instruction
        should be giving to pass it downstream for execution.
        """
        if v <= 0:
            raise ValueError("Provide a sequence value higher than 0")
        return v

    @validator('cmd')
    def cmd_should_match_seq(cls, v, values):
        """
        The number of commands for execution should match the indicated
        number of instructions, else it means that one command is missing.
        """
        if values:
            check_matching_list_sequences(v, values['seq'])
        return v

    @validator('arg')
    def arg_should_match_cmd(cls, v, values):
        """
        Check wether the list of arguments matches the expected number of
        parameters.
        """
        if values:
            try:
                check_matching_list_sequences(v, len(values['cmd']))
                return v
            except KeyError:
                pass


class Message(BaseModel):
    """
    Expected Model to be recieved trough transmission protocol.

    Attributes
    ----------
    body: Instructions
        An `instructions` model containing all the necessary information.
    creation_date: datetime.datetime, default = datetime.datetime.now()
        An optional field to indicate the creation time of this specific
        payload.
    """
    body: Instructions
    creation_date: datetime = Field(default_factory=datetime.now())
