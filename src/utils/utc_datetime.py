from datetime import datetime, timezone

from pydantic.datetime_parse import parse_datetime


class utc_datetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime  # default pydantic behavior
        yield cls.ensure_tzinfo

    @classmethod
    def ensure_tzinfo(cls, v):
        # if TZ isn't provided, we assume UTC, but you can do w/e you need
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        # else we convert to utc
        return v.astimezone(timezone.utc)
    
    @staticmethod
    def to_str(dt:datetime) -> str:
        return dt.isoformat() # replace with w/e format you want