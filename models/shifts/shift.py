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
        is_starts_or_ends_in_the_same_time = True
        is_overlap_shifts = False

        if ((shift_to_compare.start_time <= self.start_time <= shift_to_compare.end_time) or
                (self.start_time <= shift_to_compare.start_time <= self.end_time <= shift_to_compare.end_time)):
            is_overlap_shifts = True

        if self.start_time == shift_to_compare.end_time or self.end_time == shift_to_compare.start_time:
            is_starts_or_ends_in_the_same_time = False  # This shifts does not overlap

        return is_overlap_shifts and is_starts_or_ends_in_the_same_time
