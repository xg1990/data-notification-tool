from typing import Dict, List, Tuple, Optional
import numpy as np
from dnt.core.utils import (
    NOTSET,
    lvl_to_num
)
from dnt.core.base import (
    BaseFormatter,
    BaseFilterer
)


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

class MsgRcv:
    """
    A message receiver class to dispatch messages to each destination of a specific message group.
    """
    def __init__(self, config: Dict, formatter_dic: Dict, filterer_dic: Dict) -> None:
        """
        Initialize the message receiver with a config, and formatter/filterer settings.

        Args:
            config (dict): The config of the message receiver
            formatter_dic (dict): A dict of formatter settings
            filterer_dic (dict): A dict of filterer settings

        Returns:
            None
        """
        self.config = config
        self.dest = self.config.get("dest")
        self.level = self.config.get("level", "NOTSET")
        self.formatter_dic = formatter_dic
        self.filterer_dic = filterer_dic

        self.filterer = self.config.get("filterer") # 1 filterer or a list of filterers
        self.formatter = self.config.get("formatter") # 1 formatter
        self.formatter, self.filterer = self._load_styler()

    def _load_styler(self) -> Tuple[BaseFormatter, List[BaseFilterer]]:
        """
        Load formatter and filterer according to related settings.
        (There can only be 1 formatter, but multiple filterers)

        Args:
            None
        
        Returns:
            formatter (BaseFormatter): The formatter loaded
            filterer (list): A list of filterers loaded
        """
        formatter = None
        filterer = None
        formatter_name = self.config.get("formatter") # 1 formatter
        filterer_name = self.config.get("filterer") # 1 filterer or a list of filterers

        if formatter_name is not None:
            formatter = self.formatter_dic.get(formatter_name)

        if filterer_name is not None:
            filterer = [self.filterer_dic.get(fn) for fn in filterer_name]

        return formatter, filterer

    def _filter_msg(self, msg_ls: List[Message]) -> List:
        """
        Filter messages according to notification level and specific rules defined by filterer(s). 

        Args:
            msg_ls (list): A list of Message objects

        Returns:
            res_ls (list): The filtered list of Message objects
        """
        if self.filterer is not None:
            filterer_ls = self.filterer if isinstance(self.filterer, list) else [self.filterer]
            
            keep_flag_ls = []
            for msg in msg_ls:
                keep_flag_ls.append(
                    np.prod([f.filter(msg) for f in filterer_ls])
                )
            msg_ls = [msg for n, msg in enumerate(msg_ls) if keep_flag_ls[n] > 0]

        level = lvl_to_num(self.level)
        res_ls = [msg for msg in msg_ls if msg.lvl_no >= level]
        return res_ls
    
    def _format_msg(self, msg_ls: List[Message]) -> List:
        """
        Render the messages in a specific format, if no formatter assigned, will pass it to Destination for formatting.
        
        Args:
            msg_ls (list): A list of Message objects

        Returns:
            The formatted list of messages, or list of raw messages (if no formatter assigned)
        """
        if self.formatter is not None:
            res_ls = [self.formatter.format(msg) for msg in msg_ls]
            return res_ls
        else:
            return msg_ls
    
    def deliver_msg(self, msg_ls: List[Message], subject: Optional[str]=None):      
        """
        Deliver messages to a Destination in a dict manner.
        
        Args:
            msg_ls (list): A list of messages to be sent
            subject (str, optional): The subject of the message

        Returns:
            A dict to be deliverred to the destination
        """
        msg_ls = self._filter_msg(msg_ls)
        res_ls = self._format_msg(msg_ls)
        return (
            self.dest, 
            {
                "subject": subject, 
                "messages": res_ls
            }
        )

class MsgGrp:
    """
    A message group class to dispatch messages to the destinations assigned in the group.
    """
    def __init__(self, name: str, config: List, formatter_dic: Dict, filterer_dic: Dict) -> None:
        """
        Initilize the function with the message group's name, config, and formatter/filterer settings.

        Args:
            name (str): The name of the message group
            config (List): A list of message receiver settings
            formatter_dic (dict): The formatter settings on message group level
            filterer_dic (dict): The filterer settings on message group level

        Returns:
            None
        """
        self.name = name
        self.config = config
        self.formatter_dic = formatter_dic
        self.filterer_dic = filterer_dic
        
    def deliver_msg(self, msg_ls: List[Message], subject: Optional[str]=None):
        """
        Generate the messages to be deliverred to all the destinations in the group.

        Args:
            msg_ls (list): A list of messages to be sent
            subject (str, optional): The subject of the message

        Returns:
            A list of dict (with destination, subject and messages) to be deliverred
        """
        res_ls = []
        for cfg in self.config:
            rcv = MsgRcv(cfg, self.formatter_dic, self.filterer_dic)
            res_ls.append(rcv.deliver_msg(msg_ls, subject))
        return res_ls
