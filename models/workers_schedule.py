from .employees.employee import Employee
from .shifts.shift import Shift


class WorkersWeekSchedule:
    def __init__(self, week_schedule: list[tuple[Employee, Shift]]):
        self.week_schedule = week_schedule         # The finalized schedule.
    