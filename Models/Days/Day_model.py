from dataclasses import dataclass
from typing import List

from Models.Day_related.Days_enum import DaysEnum
from Models.Shifts_model import Shifts


@dataclass
class Day:

    today_is: DaysEnum
    shifts: List[Shifts]
