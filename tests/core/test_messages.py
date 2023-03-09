import pytest
from dnt.core.messages import MsgRcv, MsgGrp


def test_msg_rcv():
    """
    Test the MsgRcv class.
    """
    rcv = MsgRcv(
        config={
            "dest": "console",
            "level": "ERROR"
        },
        formatter_dic={},
        filterer_dic={}
    )
    assert rcv.config == {
        "dest": "console",
        "level": "ERROR"
    }
    assert rcv.dest == "console"
    assert rcv.level == "ERROR"
    assert rcv.formatter_dic == {}
    assert rcv.filterer_dic == {}
    assert rcv.formatter is None
    assert rcv.filterer is None
