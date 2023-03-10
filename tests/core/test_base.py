import pytest
from dnt.core.base import Message, BaseFormatter
from dnt.core.utils import INFO


def test_message():
    """
    Test the Message class.
    """
    message_dic = {
        "a": 1,
        "b": "abc",
        "level": "INFO"
    }

    msg_a = Message(message_dic)
    msg_b = Message(message_dic)

    assert msg_a.level == "INFO"
    assert msg_a.lvl_no == INFO
    assert msg_a.message == message_dic
    assert msg_a == msg_b

def test_base_formatter():
    """
    Test the BaseFormatter class.
    """
    bf = BaseFormatter()
    msg = Message({"a": 1})
    assert bf.format(msg) == "{'a': 1}"
