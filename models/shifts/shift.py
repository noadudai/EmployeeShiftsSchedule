import datetime
from dataclasses import dataclass
import uuid

from .shifts_types_enum import ShiftTypesEnum


@dataclass(frozen=True)
class Shift:
    shift_id: uuid.UUID
    shift_type: ShiftTypesEnum
    start_time: datetime.datetime
    end_time: datetime.datetime

    def overlaps_with(self, shift_to_compare: 'Shift') -> bool:
        shift_start_time_smaller_then_other_shift_end_time = self.start_time < shift_to_compare.end_time
        shift_end_time_bigger_then_other_shift_start_time = self.end_time > shift_to_compare.start_time

        return shift_start_time_smaller_then_other_shift_end_time and shift_end_time_bigger_then_other_shift_start_time
