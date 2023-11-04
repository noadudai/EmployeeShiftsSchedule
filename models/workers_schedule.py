from typing import List

from .shifts.shift import Shift


class WorkersSchedule:
    
    def __init__(self, shifts: List[Shift]):
        self.week_schedule = shifts         # The finalized schedule.
    