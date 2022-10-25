"""
Suite of tests for data models for incoming data.
"""

from pyliquid import models

def test_instructions():
    """
    Test validators from Instructions Model.
    """
    try:
        first = models.Instructions(seq=0, cmd=[(0, "cmd_1")], 
                                    arg=[(0, "arg_1")])
    except ValueError:
        pass # Should failed due to seq being 0.

    second = models.Instructions(seq=1, cmd=[(1, "cmd_1")])
    assert second.dict() == {'seq': 1, 'cmd': [(1, 'cmd_1')], 'arg': None}

    try:
        third = models.Instructions(seq=2, cmd=[(1, "cmd_1")], 
                                    arg=[(1, "arg_1")])
    except ValueError:
        pass # Should failed as length does not match seq.
