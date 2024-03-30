import datetime
from dataclasses import dataclass

from models.shifts.shifts_types_enum import ShiftTypesEnum


@dataclass
class ShiftsPreference:
    day_date: datetime.date
    shifts: list[ShiftTypesEnum]
