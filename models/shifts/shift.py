import datetime
from dataclasses import dataclass
import uuid

from .shifts_types_enum import ShiftTypesEnum


@dataclass
class Shift:
    shift_id: uuid.UUID
    shift_type: ShiftTypesEnum
    start_time: datetime.datetime
    end_time: datetime.datetime
