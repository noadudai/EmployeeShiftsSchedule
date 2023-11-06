from typing import List

from .shifts.shift import Shift


class WorkersWeekSchedule:
    
    def __init__(self, week_schedule: list):
        self.week_schedule = week_schedule         # The finalized schedule.
    