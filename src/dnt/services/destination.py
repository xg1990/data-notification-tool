import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dnt.core.base import BaseDestination, Message
from typing import List, Dict, Optional, Callable


class ClsService(BaseDestination):
    def send_messages(self, msg_ls: List, subject: Optional[str]=None, **kwargs) -> None:
        print("Message from cls service:")
        print(f"Subject: {subject}")
        for msg in msg_ls:
            print(msg)
        print("\n")

class SMTPService(BaseDestination):
    def __init__(self, name: str, host: str, port: int, username: str, password: str) -> None:
        super().__init__(name)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def send_messages(self, msg_ls: List, receivers: List, subject: Optional[str]=None, **kwargs) -> None:
        email_msg: MIMEMultipart = MIMEMultipart()
        email_msg["From"] = self.username
        email_msg["To"] = ", ".join(receivers)
        email_msg["Subject"] = subject
        body: str = ""

        for msg in msg_ls:
            body += f"- {msg}\n"

        email_msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.send_message(email_msg)
