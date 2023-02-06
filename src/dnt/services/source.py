from dnt.core.base import BaseSource, Message
from typing import List, Dict, Optional, Callable
from sqlalchemy import create_engine
import pandas as pd


class SQLSource(BaseSource):
    """
    A class to get message from SQL database.
    """
    def __init__(self, name: str, **kwargs: Dict) -> None:
        """
        Initialize the SQLSource with a name and connection configs.

        Args:
            name (str): The name of the source

        Returns:
            None
        """
        super().__init__(name)
        self.connection = create_engine(**kwargs)

    def get_messages(self, query: str) -> List[Message]:
        """
        Extract messages from the SQL database using a query.
        (Note: The query must return a column named 'level')

        Args:
            query (str): The query to extract messages

        Returns:
            msg_ls (list): A list of messages (in Message objects)
        """
        df: pd.DataFrame = pd.read_sql_query(query, con=self.connection)
        try:
            assert "level" in df.columns
        except AssertionError:
            raise AttributeError("No 'level' column in table.")

        res_ls = df.to_dict("records")
        msg_ls = [Message(msg) for msg in res_ls]
        return msg_ls
        