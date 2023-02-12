import pytest
from dnt.core.utils import (
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    NOTSET,
    lvl_to_num
)


@pytest.mark.parametrize(
    "level, expected",
    [
        (15, 15),
        (10.2, 10.2),
        ("debug", DEBUG),
        ("DEBUG", DEBUG),
        ("info", INFO),
        ("INFO", INFO),
        ("warning", WARNING),
        ("WARNING", WARNING),
        ("error", ERROR),
        ("ERROR", ERROR),
        ("critical", CRITICAL),
        ("CRITICAL", CRITICAL),
        ("notset", NOTSET),
        ("NOTSET", NOTSET),
        ("NoTsEt", NOTSET),
    ]
)
def test_lvl_to_num(level, expected):
    """
    Test the lvl_to_num function.
    """
    assert lvl_to_num(level) == expected

def test_lvl_to_num_unknown_error():
    """
    Test the lvl_to_num function with unknown level error.
    """
    with pytest.raises(ValueError):
        lvl_to_num("blahblah")

