from typing import List
import pytest
from dnt.core.base import Message
from dnt.services.source import SQLSource


def test_sqlsource():
    """
    Test the SQLSource class.
    """
    service_name: str = "subject message"
    ss = SQLSource(url="sqlite:///:memory:", name=service_name)
    msg: List[Message] = ss.get_messages(
        """
        SELECT 
            'test message from SQLite in Memory' AS msg,
            'DEBUG' AS level
        """
    )
    assert ss.name == service_name 
    assert isinstance(msg, list)
    assert msg[0] == Message(
        {
            "msg": "test message from SQLite in Memory", 
            "level": "DEBUG"
        }
    )

def test_sqlsource_nolevel_error():
    """
    Test exception on the SQLSource class due to no level defined.
    """
    service_name: str = "subject message"
    ss = SQLSource(url="sqlite:///:memory:", name=service_name)
    with pytest.raises(AttributeError):
        msg: List[Message] = ss.get_messages(
            """
            SELECT 
                'test message from SQLite in Memory' AS msg
            """
        )
