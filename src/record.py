from typing import Any
from pydantic import BaseModel, validator
from datetime import datetime

from autofastdantic.src.utils.hiddenid import MagicId

class Record(BaseModel):
    id: MagicId
    model: str
    content: Any
    created_at: datetime = None
    updated_at: datetime = None

