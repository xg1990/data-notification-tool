from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import numpy as np
from dnt.core.utils import lvl_to_num, NOTSET


class Message:
    """
    A class to store a message with extra information (e.g. notification level).
    """
    def __init__(self, msg: Dict):
        """
        Initialize the message with a dict.

        Args:
            msg (dict): The content of the message in a dict

        Returns:
            None
        """
        self.level = msg.get("level", NOTSET)
        self.lvl_no = lvl_to_num(self.level)
        self.message = msg

    def __eq__(self, other):
        return (self.lvl_no == other.lvl_no and self.message == other.message)

    def items(self):
        return self.message.items()

class BaseSource(ABC):
    """
    A base class of the source. The data to trigger the notification(s) will be 
    extracted from the source.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize the source with a name.

        Args:
            name (str): The name of the source

        Returns:
            None
        """
        self.name = name

    @abstractmethod
    def get_messages(self, **kwargs) -> List[Message]:
        """
        Extract messages from the source and wrap into a list of Message objects.
        
        Args:
            None

        Returns:
            A list of Message objects
        """
        raise NotImplementedError()


class BaseDestination(ABC):
    """
    A base class of the destination, i.e. the receiver of the notification(s).
    """
    def __init__(self, name, **kwargs) -> None:
        """
        Initialize the destination with a name and other settings.

        Args:
            name (str): The name of the destination

        Returns:
            None
        """
        self.name = name
        self.level = kwargs.get("level", "NOTSET")
        self.filterer = kwargs.get("filterer") # 1 filterer or a list of filterers
        self.formatter = kwargs.get("formatter") # 1 formatter

    def _filter_msg(self, msg_ls: List[Message]) -> List:
        """
        Filter messages according to notification level and specific rules defined by filterer(s).
        (This will be overwhelmed by the level & filtering settings in message_groups.)

        Args:
            msg_ls (list): A list of Message objects

        Returns:
            res_ls (list): The filtered list of Message objects
        """
        if self.filterer is not None:
            filterer_ls = self.filterer if isinstance(self.filterer, list) else [self.filterer]
            
            keep_flag_ls = []
            for msg in msg_ls:
                if isinstance(msg, Message):
                    keep_flag_ls.append(
                        np.prod([f.filter(msg) for f in filterer_ls])
                    )
                else:
                    keep_flag_ls.append(1)
            msg_ls = [msg for n, msg in enumerate(msg_ls) if keep_flag_ls[n] > 0]

        level = lvl_to_num(self.level)
        res_ls = []
        for msg in msg_ls:
            if isinstance(msg, Message):
                if msg.lvl_no >= level:
                    res_ls.append(msg)
            else:
                res_ls.append(msg)
        return res_ls

    def _format_msg(self, msg_ls: List[Message]) -> List:
        """
        Render the message(s) in a specific format as text, if no formatter defined, will simply 
        stringify message(s).

        Args:
            msg_ls (list): A list of Message objects

        Returns:
            res_ls (list): The formatted list of messages
        """
        formatter = BaseFormatter() if self.formatter is None else self.formatter()
        res_ls = [formatter.format(msg) if isinstance(msg, Message) else msg for msg in msg_ls]

        return res_ls

    @abstractmethod
    def send_messages(self, msg_ls: List, subject: Optional[str]=None, **kwargs) -> None:
        """
        Send the messages using the API of receiver(s) (e.g. email via SMTP).

        Args:
            msg_ls (list): A list of messages to be sent
            subject (str, optional): The subject of the message, None by default

        Returns:
            None
        """
        raise NotImplementedError()

    def emit(self, msg_ls: List[Message], subject: Optional[str]=None, **kwargs) -> None:
        """
        The process to filter, format and send the messages.

        Args:
            msg_ls (list): A list of messages to be sent
            subject (str, optional): The subject of the message, None by default
        
        Returns:
            None
        """
        msg_ls = self._filter_msg(msg_ls)
        res_ls = self._format_msg(msg_ls)
        params = {"msg_ls": res_ls, "subject": subject, **kwargs}
        self.send_messages(**params)


class BaseFormatter(ABC):
    """
    A base class of formatter, which is used to render a Message object into text.
    """
    def format(self, msg: Message):
        """
        Render a Message object into text.

        Args:
            msg (Message): A Message object to be renderred

        Return:
            The stringified message
        """
        return str(msg.message)


class BaseFilterer(ABC):
    """
    A base class of filterer to check whether to filter a message or not, work on each single message.
    """
    @abstractmethod
    def filter(self, msg: Message) -> bool:
        """
        Classify whether a message should be sent according to specific rules.

        Args:
            msg (Message): A Message object to be filtered

        Returns:
            Whether a message should be sent
        """
        raise NotImplementedError()
