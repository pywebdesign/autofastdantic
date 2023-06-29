from typing import List, Optional

from pydantic import BaseModel

from .record import Record


class Response(BaseModel):
    record: Optional[Record]
    records: Optional[List[Record]]