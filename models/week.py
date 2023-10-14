from dataclasses import dataclass
from typing import List

from models.days.day import Day


@dataclass
class Week:
    days_in_this_week: List[Day]
