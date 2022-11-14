from typing import List

import pydantic


class Messages(pydantic.BaseModel):
    subject: str
    messages: List[str] = []
