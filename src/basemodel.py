from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, validator
from .utils.hiddenid import int_to_hash

class BaseModel(PydanticBaseModel):
    class _Access:
        List = False
        Create = True
        Update = True
        
class Loggable():
    class _Login:
        retreive_field: "email"