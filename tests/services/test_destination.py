from typing import List
import pytest
import smtplib
from dnt.core.base import Message
from dnt.services.destination import ClsService, SMTPService


def test_clsservice(capfd):
    """
    Test the ClsService class.
    """
    service_name: str = "cls_test"
    cs = ClsService(name=service_name)
    assert cs.name == service_name
    assert cs.level == "NOTSET"

    cs.send_messages(["Hello World!"], subject="Test Message")
    out, err = capfd.readouterr()
    assert out == "Message from cls service:\nSubject: Test Message\nHello World!\n\n\n"

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
