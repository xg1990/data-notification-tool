from typing import List
import pytest
import smtplib
from email.mime.multipart import MIMEMultipart
from unittest.mock import patch
from dnt.core.base import Message
from dnt.services.destination import ClsService, SMTPService


@pytest.mark.parametrize(
    "msg_ls, subject, level, expected_out",
    [
        (
            ["Hello World!"],
            "Test Message",
            None,
            "Message from cls service:\nSubject: Test Message\nHello World!\n\n\n"
        ),
        (
            [
                Message({"a": 100, "level": "INFO"}),
                Message({"a": 5, "level": "ERROR"}),
            ],
            "New",
            "ERROR",
            "Message from cls service:\nSubject: New\n{'a': 5, 'level': 'ERROR'}\n\n\n"
        )
    ]
)
def test_clsservice(
    msg_ls, 
    subject, 
    level, 
    expected_out, 
    capfd
):
    """
    Test the ClsService class.
    """
    service_name: str = "cls_test"
    if level is None:
        cs = ClsService(name=service_name)
        assert cs.level == "NOTSET"
    else:
        cs = ClsService(name=service_name, level=level)
        assert cs.level == level
    assert cs.name == service_name

    cs.emit(msg_ls, subject=subject)
    out, err = capfd.readouterr()
    assert out == expected_out

def test_smtpservice():
    """
    Test the SMTPService class.
    """
    service_name: str = "smtp_test"
    ss = SMTPService(
        name=service_name,
        host="smtp.gmail.com",
        port=587,
        username="abc@gmail.com",
        password="123456"
    )

    assert ss.host == "smtp.gmail.com"
    assert ss.port == 587
    assert ss.username == "abc@gmail.com"
    assert ss.password == "123456"

    with patch("smtplib.SMTP") as mock_smtp:
        ss.send_messages(
            msg_ls=["Hello World!"],
            receivers=["def@gmail.com"],
            subject="Test Message"
        )

        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with(
            "abc@gmail.com",
            "123456"
        )
        
        msg = mock_smtp.return_value.send_message.call_args[0][0]
        assert isinstance(msg, MIMEMultipart)
        assert msg["From"] == "abc@gmail.com"
        assert msg["To"] == "def@gmail.com"
        assert msg["Subject"] == "Test Message"
        assert len(msg.get_payload()) == 1
        assert "Hello World!" in msg.get_payload()[0].as_string()
