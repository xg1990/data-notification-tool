from dnt.core.messages import Messages
from dnt.services.sql import SQLSource


def test_sql_service():
    service_name: str = "subject message"
    ss = SQLSource(url="sqlite:///:memory:", name=service_name)
    msg: Messages = ss.get_messages(
        "SELECT 'test message from SQLite in Memory'"
    )
    assert msg == Messages(
        subject=service_name, messages=["test message from SQLite in Memory"]
    )
