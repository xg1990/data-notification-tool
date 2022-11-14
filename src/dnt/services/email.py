import smtplib
from email.mime.multipart import MIMEMultipart
from typing import List

from dnt.core.messages import Messages
from dnt.core.service import MessageServiceBase


class SMTPService(MessageServiceBase):
    def __init__(
        self, name, host: str, port: int, username: str, password: str
    ) -> None:
        super().__init__(name)
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def send_messages(self, msg_list: List[Messages], receivers) -> None:

        msg: MIMEMultipart = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = ", ".join(receivers)
        msg["Subject"] = "|".join([msg.subject for msg in msg_list])

        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.send_message(msg)
