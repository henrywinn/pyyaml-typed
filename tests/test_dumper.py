import random
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Callable, NamedTuple, Optional, Union

import pytest

from tyaml import dump


def cls_variant() -> Callable[[int, str], Any]:
    @dataclass
    class ExampleDataClass:
        int_field: int
        str_field: str

    yield ExampleDataClass

    @dataclass(frozen=True)
    class ExampleDataClassFrozen:
        int_field: int
        str_field: str

    yield ExampleDataClassFrozen

    yield namedtuple("ExampleNamedTuple", ["int_field", "str_field"])

    class ExampleTypedNamedTuple(NamedTuple):
        int_field: int
        str_field: str

    yield ExampleTypedNamedTuple

    class SimpleCommentedClass:
        int_field: int  # yaml: int_field
        str_field: str  # yaml: str_field
        other_field: str = 'asd'

        def __init__(self, i_fld, s_fld):
            self.int_field = i_fld
            self.str_field = s_fld

    yield SimpleCommentedClass

    @dataclass
    class ClassFieldRenamed:
        int_field: int
        not_str_field: str  # yaml: str_field

    yield ClassFieldRenamed


# @pytest.mark.parametrize("cls", cls_variant())
# def test_typed_fields(cls):
#     int_field = random.randrange(100)
#     str_field = "fhjldgfhjsdfgj"
#
#     res = dump(cls(int_field, str_field))
#     assert res == f"int_field: {int_field}\nstr_field: {str_field}\n"
#
#
# def test_plain_class():
#     class ThatClass:
#         int_field: int
#         str_field: str
#
#         def __init__(self, i_fld, s_fld):
#             self.int_field = i_fld
#             self.str_field = s_fld
#
#     res = dump(ThatClass(1, "2"))
#     assert res == "!!python/object:test_dumper.ThatClass\nint_field: 1\nstr_field: '2'\n"
    
def test_no_write_optional_null():
    class MixedOptionalFields:
        int_or_none_field: Union[int, None]
        optional_int_field: Optional[int]
        
        def __init__(self, i_or_none, optional_int):
            self.int_or_none_field = i_or_none
            self.optional_int_field = optional_int
    
    test_cases = [
        # Where output_null_optionals = False
        (
            False,
            MixedOptionalFields(None, None),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: null\n"
        ),
        (
            False,
            MixedOptionalFields(1, None),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: 1\n"
        ),
        (
            False,
            MixedOptionalFields(None, 2),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: null\noptional_int_field: 2\n"
        ),
        (
            False,
            MixedOptionalFields(1, 2),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: 1\noptional_int_field: 2\n"
        ),
        # Where output_null_optionals = True
        (
            True,
            MixedOptionalFields(None, None),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: null\noptional_int_field: null\n"
        ),
        (
            True,
            MixedOptionalFields(1, None),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: 1\noptional_int_field: null\n"
        ),
        (
            True,
            MixedOptionalFields(None, 2),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: null\noptional_int_field: 2"
        ),
        (
            True,
            MixedOptionalFields(1, 2),
            "!!python/object:test_dumper.MixedOptionalFields\nint_or_null_field: 1\noptional_int_field: 2"
        ),
    ]
    
    for output_null_optionals, class_instance, expected_result in test_cases:
        actual_result = dump(class_instance, output_null_optionals=output_null_optionals)
        assert actual_result == expected_result
            
    
