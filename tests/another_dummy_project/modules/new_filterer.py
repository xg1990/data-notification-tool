from dnt.core.messages import Message
from dnt.core.base import BaseFilterer


class SqlServerFilterer(BaseFilterer):
    @staticmethod
    def filter(msg: Message) -> bool:
        res = False
        if msg.message["db"] == "sqlserver":
            res = True
        return res

class DevFilterer(BaseFilterer):
    @staticmethod
    def filter(msg: Message) -> bool:
        res = False
        if "dev" in msg.message["table_name"]:
            res = True
        return res
