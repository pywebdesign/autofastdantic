
import base64
import hashlib
import bcrypt

class MagicPassword():
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if v is None:
            raise ValueError("password not provided")
        if isinstance(v, str):
            return 
        raise ValueError(f'invalid value for id -> hashid, {v}')
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", example="['ksjdhf*?tfg&?$srf', ')(EUR&?T/GHNJVED&)']")
