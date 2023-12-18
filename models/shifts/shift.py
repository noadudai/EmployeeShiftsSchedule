import datetime
from dataclasses import dataclass
from uuid import uuid4

from .shifts_types_enum import ShiftTypesEnum


@dataclass
class Shift:
    shift_id: uuid4
    shift_type: ShiftTypesEnum
    start_time: datetime.datetime
    end_time: datetime.datetime
