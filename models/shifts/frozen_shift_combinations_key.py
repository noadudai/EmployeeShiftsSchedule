import datetime
from dataclasses import dataclass

from .shifts_types_enum import ShiftTypesEnum


@dataclass(frozen=True)
class FrozenShiftCombinationKey:
    employee_id: int
    start_date_of_shift: datetime.date
    end_date_of_shift: datetime.date
    shift_type: ShiftTypesEnum
