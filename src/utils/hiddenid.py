import hashids
hash = hashids.Hashids(salt="20d94jn5k,clzx097372y4r", min_length=7)
def int_to_hash(integer):
    return hash.encode(int(integer))

def hash_to_int(s: str):
    if s is None:
        return None
    return hash.decode(str(s))[0]


class MagicId():
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if v is None:
            return None
        if isinstance(v, int):
            return int_to_hash(v)
        if isinstance(v, str):
            return hash_to_int(v)
        raise ValueError(f'invalid value for id -> hashid, {v}')
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="Union[int, str]", example="['None']")