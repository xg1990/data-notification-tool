import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dnt.core.base import BaseDestination, Message
from typing import List, Dict, Optional, Callable


class ClsService(BaseDestination):
    """
    A class for console destination (printing messages to console).
    """
    def send_messages(self, msg_ls: List, subject: Optional[str]=None, **kwargs) -> None:
        """
        Send messages to console to display.

        Args:
            msg_ls (list): A list of messages to be sent
            subject (str, optional): The subject of the message. None by default

        Returns:
            None
        """
        print("Message from cls service:")
        print(f"Subject: {subject}")
        for msg in msg_ls:
            print(msg)
        print("\n")

class SMTPService(BaseDestination):
    """
    A class for Email destination (SMTP).
    """
    def __init__(self, name: str, host: str, port: int, username: str, password: str) -> None:
        """
        Initialize an SMTP service with name and configs.

        Args:
            name (str): The name of the service
            host (str): The host of the SMTP server
            port (int): The port of the SMTP server
            username (str): The username to login to the SMTP server
            password (str): The password to login to the SMTP server

        Returns:
            None
        """
        super().__init__(name)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def send_messages(self, msg_ls: List, receivers: List, subject: Optional[str]=None, **kwargs) -> None:
        """
        Send messages via Email to receivers.

        Args:
            msg_ls (list): A list of messages to be sent
            receivers (list): A list of receivers' email addresses
            subject (str, optional): The subject of the message. None by default

        Returns:
            None
        """
        email_msg: MIMEMultipart = MIMEMultipart()
        email_msg["From"] = self.username
        email_msg["To"] = ", ".join(receivers)
        email_msg["Subject"] = subject
        body: str = ""

        send_ls = self._filter_msg(msg_ls)
        send_ls = self._format_msg(send_ls)
        for msg in send_ls:
            body += f"- {msg}\n"

        email_msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.send_message(email_msg)
