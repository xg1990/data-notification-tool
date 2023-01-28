from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import numpy as np
from dnt.core.utils import lvl_to_num
from dnt.core.messages import Message


class BaseSource(ABC):
    """
    A base class of the source.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize the source with a name
        """
        self.name = name

    @abstractmethod
    def get_messages(self, **kwargs) -> List[Message]:
        """
        Extract messages from the source and wrap into a list of Message objects.
        """
        raise NotImplementedError()

class BaseDestination(ABC):
    """
    A base class of the destination.
    """
    def __init__(self, name, **kwargs) -> None:
        self.name = name
        self.level = kwargs.get("level", "NOTSET")
        self.filterer = kwargs.get("filterer") # 1 filterer or a list of filterers
        self.formatter = kwargs.get("formatter") # 1 formatter

    def _filter_msg(self, msg_ls: List[Message]) -> List:
        """
        Filter messages according to specific rules.
        This will be overwhelmed by the level & filtering settings in message_groups
        """
        if self.filterer is not None:
            filterer_ls = self.filterer if isinstance(self.filterer, list) else [self.filterer]
            
            keep_flag_ls = []
            for msg in msg_ls:
                if isinstance(msg, Message):
                    keep_flag_ls.append(
                        np.cumprod([f.filter(msg) for f in filterer_ls])
                    )
                else:
                    keep_flag_ls.append(1)
            msg_ls = [msg for n, msg in enumerate(msg_ls) if keep_flag_ls[n] > 0]

        level = lvl_to_num(self.level)
        res_ls = [msg if isinstance(msg, Message) and msg.lvl_no >= level else msg for msg in msg_ls]
        return res_ls

    def _format_msg(self, msg_ls: List[Message]) -> List:
        """
        Render the messages in a specific format, if no formatter assigned, will pass it to Destination for formatting.
        """
        formatter = BaseFormatter if self.formatter is None else self.formatter
        res_ls = [formatter.format(msg) if isinstance(msg, Message) else msg for msg in msg_ls]

        return res_ls

    @abstractmethod
    def send_messages(self, msg_ls: List, subject: Optional[str]=None, **kwargs) -> None:
        """
        Send the messages using the API of downstream services (e.g. email via SMTP).
        """
        raise NotImplementedError()

    def emit(self, msg_ls: List, subject: Optional[str]=None, **kwargs) -> None:
        """
        The process to filter, format and send the messages
        """
        msg_ls = self._filter_msg(msg_ls)
        res_ls = self._format_msg(msg_ls)
        self.send_messages(res_ls, subject, **kwargs)

class BaseFormatter(ABC):
    def format(self, msg: Message):
        return str(msg.message)

class BaseFilterer(ABC):
    """
    Check whether to filter a message or not, work on each single message.
    """
    @abstractmethod
    def filter(self, msg: Message) -> bool:
        raise NotImplementedError()
