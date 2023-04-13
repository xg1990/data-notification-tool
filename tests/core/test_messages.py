import pytest
from dnt.core.messages import MsgRcv, MsgGrp
from dnt.core.base import BaseFormatter, BaseFilterer, Message


# helper func/class
class SomeFilterer(BaseFilterer):
    @staticmethod
    def filter(msg: Message) -> bool:
        res = False
        if msg.message["a"] < 5:
            res = True
        return res


@pytest.mark.parametrize(
    "config, formatter_dic, filterer_dic, expected_formatter, expected_filterer, expected_n_msg",
    [
        (
            {
                "dest": "console",
                "level": "ERROR"
            },
            {},
            {},
            None,
            None,
            1
        ),
        (
            {
                "dest": "console",
                "level": "ERROR",
                "formatter": "base_formatter",
                "filterer": ["some_filterter"]
            },
            {"base_formatter": BaseFormatter()},
            {"some_filterter": SomeFilterer()},
            BaseFormatter,
            [SomeFilterer],
            0
        ),
    ]
)
def test_msg_rcv(config, formatter_dic, filterer_dic, expected_formatter, expected_filterer, expected_n_msg):
    """
    Test the MsgRcv class.
    """
    rcv = MsgRcv(
        config=config,
        formatter_dic=formatter_dic,
        filterer_dic=filterer_dic
    )
    assert rcv.config == config
    assert rcv.dest == config["dest"]
    assert rcv.level == config["level"]
    assert rcv.formatter_dic == formatter_dic
    assert rcv.filterer_dic == filterer_dic
    
    if expected_formatter is None:
        assert rcv.formatter is None
    else:
        assert isinstance(rcv.formatter, expected_formatter)
    
    if expected_filterer is None:
        assert rcv.filterer is None
    else:
        assert len(rcv.filterer) == len(expected_filterer)
        for n, i in enumerate(expected_filterer):
            assert isinstance(rcv.filterer[n], i)

    msg_ls = [
        Message({"a": 1, "b": "test", "level": "INFO"}),
        Message({"a": 10, "b": "nope", "level": "ERROR"})
    ]

    filterred_msg = rcv._filter_msg(msg_ls)
    assert isinstance(filterred_msg, list)
    for i in filterred_msg:
        assert isinstance(i, Message)
        assert len(filterred_msg) == expected_n_msg

    formatted_msg = rcv._format_msg(msg_ls)
    assert isinstance(formatted_msg, list)
    for i in formatted_msg:
        if expected_formatter is None:
            assert isinstance(i, Message)
        else:
            assert isinstance(i, str)

    dest, delivered_msg = rcv.deliver_msg(msg_ls, subject="test_test")
    assert dest == rcv.dest
    assert isinstance(delivered_msg, dict)
    assert delivered_msg["subject"] == "test_test"
    assert isinstance(delivered_msg["msg_ls"], list)
    assert len(delivered_msg["msg_ls"]) == expected_n_msg


@pytest.mark.parametrize(
    "name, config, formatter_dic, filterer_dic, expected_n_msg",
    [
        (
            "test_msg_grp",
            [
                {
                    "dest": "console",
                    "level": "ERROR",
                    "formatter": "base_formatter",
                    "filterer": ["some_filterter"]
                },
                {
                    "dest": "console",
                    "level": "DEBUG",
                    "formatter": "base_formatter",
                    "filterer": ["some_filterter"]
                }
            ],
            {"base_formatter": BaseFormatter()},
            {"some_filterter": SomeFilterer()},
            [0, 1]
        ),
    ]
)
def test_msg_grp(name, config, formatter_dic, filterer_dic, expected_n_msg):
    """
    Test the MsgGrp class.
    """
    msg_grp = MsgGrp(name, config, formatter_dic, filterer_dic)
    assert msg_grp.name == name
    assert msg_grp.config == config
    assert msg_grp.formatter_dic == formatter_dic
    assert msg_grp.filterer_dic == filterer_dic

    msg_ls = [
        Message({"a": 1, "b": "test", "level": "INFO"}),
        Message({"a": 10, "b": "nope", "level": "ERROR"})
    ]
    subject = "test_test"
    delivered_msg = msg_grp.deliver_msg(msg_ls, subject=subject)

    assert isinstance(delivered_msg, list)
    assert len(delivered_msg) == len(config)
    for n, i in enumerate(delivered_msg):
        assert isinstance(i, tuple)
        assert isinstance(i[0], str) # dest
        assert isinstance(i[1], dict) # delivered_msg
        assert isinstance(i[1]["msg_ls"], list)
        assert len(i[1]["msg_ls"]) == expected_n_msg[n]
