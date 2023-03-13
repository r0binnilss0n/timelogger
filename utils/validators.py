import re
from enum import Enum
from typing import Final

MAX_LENGT_TIME_INPUT: Final[int] = 5


class FIELDS(Enum):
    TIMEDELTA = 0


def format_special_fields(field_type: FIELDS, value: str):
    match field_type:
        case FIELDS.TIMEDELTA:
            return validate_time_field(value)
        case _:
            raise ValueError("Field type does not exist")


def validate_time_field(time: str) -> str:
    r = re.compile("[0-9]{1,2}:[0-9]{2}:[0-9]{2}")
    if r.match(time):
        return time
    assert (
        not (MAX_LENGT_TIME_INPUT - 1) < len(time) > MAX_LENGT_TIME_INPUT
    ), "Invalid time value"  #
    if ":" not in time:
        assert len(time) == (
            MAX_LENGT_TIME_INPUT - 1
        ), "Unable to add : into time value"
        time = time[:2] + ":" + time[2:]
    return time
