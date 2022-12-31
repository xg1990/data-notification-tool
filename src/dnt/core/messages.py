from typing import Dict, List, Optional
import numpy as np
from dnt.core.utils import (
    NOTSET,
    lvl_to_num
)


class Message:
    def __init__(self, msg: Dict):
        self.level = msg.get("level", NOTSET)
        self.lvl_no = lvl_to_num(self.level)
        self.message = msg

class MsgRcv:
    """
    A message receiver class to dispatch messages to each destination of a specific message group.
    """
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.dest = self.config.get("dest")
        self.level = self.config.get("level", "NOTSET")
        self.filterer = self.config.get("filterer") # 1 filterer or a list of filterers
        self.formatter = self.config.get("formatter") # 1 formatter
        
    def _filter_msg(self, msg_ls: List[Message]) -> List:
        """
        Filter messages according to specific rules.
        """
        if self.filterer is not None:
            filterer_ls = self.filterer if isinstance(self.filterer, list) else [self.filterer]
            
            keep_flag_ls = []
            for msg in msg_ls:
                keep_flag_ls.append(
                    np.cumprod([f.filter(msg) for f in filterer_ls])
                )
            
            msg_ls = [msg for n, msg in enumerate(msg_ls) if keep_flag_ls[n] > 0]

        level = lvl_to_num(self.level)
        res_ls = [msg for msg in msg_ls if msg.lvl_no >= level]
        return res_ls
    
    def _format_msg(self, msg_ls: List[Message]) -> List:
        """
        Render the messages in a specific format, if no formatter assigned, will pass it to Destination for formatting.
        """
        if self.formatter is not None:
            res_ls = [self.formatter.format(msg) for msg in msg_ls]
            return res_ls
        else:
            return msg_ls
    
    def deliver_msg(self, msg_ls: List[Message], subject: Optional[str]=None):      
        """
        Deliver messages to a Destination in a dict manner.
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
    def __init__(self, name, config: List) -> None:
        self.name = name
        self.config = config
        
    def deliver_msg(self, msg_ls: List[Message], subject: Optional[str]=None):
        """
        Delivery messages to all the destinations in the group.
        """
        res_ls = []
        for cfg in self.config:
            rcv = MsgRcv(cfg)
            res_ls.append(rcv.deliver_msg(msg_ls, subject))
        return res_ls
