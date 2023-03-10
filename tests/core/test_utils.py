import pytest
from dnt.core.utils import (
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    NOTSET,
    lvl_to_num,
    dict_drop_key,
    get_all_key_values,
    get_components
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

def test_dict_drop_key():
    """
    Test the dict_drop_key function.
    """
    dic = {"a": 1, "b": 2, "c": 3}
    assert dict_drop_key(dic, "b") == {"a": 1, "c": 3}

@pytest.mark.parametrize(
    "source_dict, key, expected",
    [
        ({"a": 1, "b": 2, "c": 3, "d": 4}, "d", [4]),
        ({"a": {"c": 1, "d": 2}, "b": {"c": 3, "e": 4}}, "c", [1, 3]),
        ({"a": [{"c": 2, "d": 1}, {"c": 3, "d": 3}]}, "c", [2, 3]),
    ]
)
def test_get_all_key_values(source_dict, key, expected):
    """
    Test the get_all_key_values function.
    """
    assert list(get_all_key_values(source_dict, key)) == expected

@pytest.mark.parametrize(
    "config_dict, comp_name, expected",
    [
        (
            {
                "grp": {}
            }, "formatter", []
        ),
        (
            {
                "grp": [
                    {
                        "dest": "blah",
                        "formatter": "blahblah",
                        "level": "blahblahblah"
                    },
                    {
                        "dest": "ok",
                        "formatter": "okok",
                        "level": "okokok"
                    }
                ]
            }, "formatter", ["blahblah", "okok"]
        ),
        (
            {
                "grp": [
                    {
                        "dest": "blah",
                        "filterer": "blahblah"
                    },
                    {
                        "dest": "ok",
                        "filterer": ["okok", "good"]
                    }
                ]
            }, "filterer", ["blahblah", "okok", "good"]
        ),
    ]
)
def test_get_components(config_dict, comp_name, expected):
    """
    Test the get_components function.
    """
    res = get_components(config_dict, comp_name)
    assert isinstance(res, list)
    assert res == list(set(expected))
