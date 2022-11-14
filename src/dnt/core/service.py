import abc
import pydoc
import sys
from typing import Any, Dict, List, Type

import pydantic

import dnt
from dnt.core.messages import Messages
from dnt.core.utils import dict_drop_key


class ServiceBase(abc.ABC):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def get_messages(self, subject: str, **kwargs) -> Messages:
        raise NotImplementedError()

    def send_messages(self, msg_list: List[Messages], **kwargs) -> None:
        raise NotImplementedError()


class DataServiceBase(ServiceBase):
    @abc.abstractmethod
    def get_messages(self, subject: str, **kwargs) -> Messages:
        raise NotImplementedError()


class MessageServiceBase(ServiceBase):
    @abc.abstractmethod
    def send_messages(self, msg_list: List[Messages], **kwargs) -> None:
        raise NotImplementedError()


def build_service(service_config: Dict, service_name: str):
    class_name = service_config["class_name"]
    _cls: Type[ServiceBase] = pydoc.locate(class_name)  # type: ignore
    if _cls is None:
        _cls: Type[ServiceBase] = pydoc.locate(f"dnt.services.{class_name}")
        if _cls is None:
            raise ValueError(f"The Service Class `{class_name}` is not found")
    return _cls(name=service_name, **dict_drop_key(service_config, "class_name"))
