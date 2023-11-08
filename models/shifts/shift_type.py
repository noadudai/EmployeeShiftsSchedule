import datetime
from dataclasses import dataclass

from .shifts_types_enum import ShiftTypesEnum


@dataclass
class ShiftType:
    name_of_shift: ShiftTypesEnum
    start_time: datetime.time
    end_time: datetime.time
