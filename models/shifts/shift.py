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

    def parallel_to(self, shift_to_compare: 'Shift') -> bool:
        return (shift_to_compare.start_time <= self.start_time <= shift_to_compare.end_time) \
                or (shift_to_compare.start_time >= self.start_time >= shift_to_compare.start_time)
