"""
Suite of tests for module data from subpackage utils
"""

# General imports
from decimal import Decimal
# Module imports
from pyliquid.utils.data import parse_decimal_to_float


def test_decimal_float_parser():
    """
    Test validators for dict type casting
    """
    expected_one = {"first": 1.0, "second": "two", 
            "third": {"sub": 1.0}}
    result_one = parse_decimal_to_float({"first": Decimal(1), 
            "second": "two", "third": {"sub": Decimal(1)}})
    expected_two = {"first": {"second": 1.0, "third": 1}}
    result_two = parse_decimal_to_float({"first": 
        {"second": Decimal(1), "third": 1}})
    expected_three = {"first": {"second": {"third": 1.0}}}
    result_three = parse_decimal_to_float({"first": {"second": {
                                            "third": Decimal(1)}}})
    assert expected_one == result_one
    assert expected_two == result_two
    assert expected_three == result_three
