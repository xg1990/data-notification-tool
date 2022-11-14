from typing import List, Optional
from dnt.core.service import Messages, ServiceBase


class DummyService(ServiceBase):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def _validate_exec_kwargs(self, kwargs) -> None:
        pass

    def get_messages(self, **kwargs) -> Messages:
        self._validate_exec_kwargs(kwargs)
        return Messages(
            subject=f"MESSAGE FROM DUMMY SERVICE [{self.name}]",
        )

    def send_messages(self, msg_list: List[Messages], **kwargs) -> None:
        print(f"MESSAGE FROM DUMMY SERVICE [{self.name}]")
        for i, msg in enumerate (msg_list):
            print(f"MESSAGE {i}")
            print(f"Subject: {msg.subject}")
            print(f"Contents: {msg.messages}")
