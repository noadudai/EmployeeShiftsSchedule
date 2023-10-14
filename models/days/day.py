from dataclasses import dataclass
from typing import List

from .days_enum import DaysEnum
from models.shifts.shift import Shift


@dataclass
class Day:

    today_is: DaysEnum
    shifts: List[Shift]
