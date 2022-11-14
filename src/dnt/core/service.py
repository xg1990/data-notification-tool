import sys
import abc
import pydoc
from typing import Any, Dict, List
from dnt.core.utils import dict_drop_key
import pydantic


class ExecutionResult(pydantic.BaseModel):
    flag: bool
    short_msg: Any = ""
    message: Any = ""


class Messages(pydantic.BaseModel):
    subject: str
    messages: List[str] = []


class ServiceBase(abc.ABC):
    def __init__(self) -> None:
        super().__init__()
    def get_messages(self, **kwargs) -> Messages:
        raise NotImplementedError()
    def send_messages(self, msg_list: List[Messages], **kwargs) -> None:
        raise NotImplementedError()

class DataServiceBase(ServiceBase):
    @abc.abstractmethod
    def get_messages(self, **kwargs) -> Messages:
        raise NotImplementedError()

class MessageServiceBase(ServiceBase):
    @abc.abstractmethod
    def send_messages(self, msg_list: List[Messages], **kwargs) -> None:
        raise NotImplementedError()

def build_service(service_config: Dict):
    class_name = service_config["class_name"]
    _cls = pydoc.locate(class_name)
    if _cls is None:
        raise ValueError(f"The Service Class `{class_name}` is not found")
    return _cls(**dict_drop_key(service_config, "class_name"))
