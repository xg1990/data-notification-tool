from dnt.core.base import BaseSource, Message
from typing import List, Dict, Optional, Callable
from sqlalchemy import create_engine
import pandas as pd


class SQLSource(BaseSource):
    def __init__(self, name: str, **kwargs: Dict) -> None:
        super().__init__(name)
        self.connection = create_engine(**kwargs)

    def get_messages(self, query: str) -> List[Message]:
        df: pd.DataFrame = pd.read_sql_query(query, con=self.connection)
        try:
            assert "level" in df.columns
        except AssertionError:
            raise AttributeError("No 'level' column in table.")

        res_ls = df.to_dict("records")
        msg_ls = [Message(msg) for msg in res_ls]
        return msg_ls
        